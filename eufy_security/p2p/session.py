import asyncio
from collections import defaultdict
from enum import Enum
import ipaddress
import logging
import math
import socket
from typing import List, Tuple

from .connection_manager import ConnectionManager
from .discovery import DiscoveryP2PClientProtocol, LocalDiscoveryP2PClientProtocol
from .lib32100 import BaseP2PClientProtocol
from .types import (
    CommandType,
    EufyP2PDataType,
    P2PClientProtocolRequestMessageType,
    P2PClientProtocolResponseMessageType,
)

_LOGGER: logging.Logger = logging.getLogger(__name__)


# These seem to be hardcoded
SEEDS = [
    "34.235.4.153",
    "54.153.101.7",
    "18.223.127.200",
    # EU discovery contacts
    "54.223.148.206",
    "18.197.212.165",
    "13.251.222.7",
]


class EufyP2PClientProtocol(BaseP2PClientProtocol):
    def __init__(self, loop, p2p_did, connection_success):
        self.loop = loop
        self.p2p_did = p2p_did
        self.connection_success = connection_success
        self.transport = None
        self.acks = defaultdict(list)
        self.keepalive_task = None
        self.seqno = 0
        self.pending = {}
        self.seen = defaultdict(lambda: -1)

    def wait_for(self, coroutine):
        asyncio.ensure_future(self.loop.create_task(coroutine))

    def send(self, data):
        if self.transport and not self.transport.is_closing():
            self.transport.sendto(data, self.addr)

    def close(self):
        self.send(self.create_message(P2PClientProtocolRequestMessageType.END))

    def connection_made(self, transport, addr):
        self.transport = transport
        self.addr = addr

        p2p_did_components = self.p2p_did.split("-")
        payload = bytearray(p2p_did_components[0].encode())
        payload.extend(int(p2p_did_components[1]).to_bytes(5, byteorder="big"))
        payload.extend(p2p_did_components[2].encode())
        payload.extend([0x00, 0x00, 0x00])

        # Attempt to create session with hub
        for _ in range(4):
            self.send(
                self.create_message(
                    P2PClientProtocolRequestMessageType.CHECK_CAM, payload
                )
            )

        # Manually timeout if we don't get an answer
        self.loop.create_task(self.timeout(1))

    async def timeout(self, seconds: float):
        await asyncio.sleep(seconds)
        if not self.keepalive_task:
            if not self.connection_success.done():
                self.connection_success.set_result(False)

    async def keepalive(self):
        ping_tick = 0
        while True:
            # Ack packets before sending a ping
            for ack_type in EufyP2PDataType:
                pending_acks = self.acks[ack_type]
                num_pending_acks = len(pending_acks)
                if num_pending_acks > 0:
                    payload = bytearray(ack_type.value)
                    payload.extend(
                        [math.floor(num_pending_acks / 256), num_pending_acks % 256]
                    )
                    for seq in pending_acks:
                        payload.extend([math.floor(seq / 256), seq % 256])

                    self.send(
                        self.create_message(
                            P2PClientProtocolRequestMessageType.ACK, payload
                        )
                    )
                    self.acks[ack_type] = []

            # Send a ping every 1s
            if ping_tick == 0:
                self.send(self.create_message(P2PClientProtocolRequestMessageType.PING))
            ping_tick = (ping_tick + 1) % 20

            await asyncio.sleep(0.05)

    def process_response(
        self,
        msg_type: P2PClientProtocolResponseMessageType,
        payload: bytes,
        addr: Tuple[str, int],
    ):
        if msg_type == P2PClientProtocolResponseMessageType.PONG:
            return

        if (
            not self.connection_success.done()
            and msg_type == P2PClientProtocolResponseMessageType.CAM_ID
        ):
            self.keepalive_task = self.loop.create_task(self.keepalive())
            self.send(self.create_message(P2PClientProtocolRequestMessageType.PING))

            # Wait for eufy protocol level ping response
            self.wait_for(
                self.async_send_command(
                    CommandType.CMD_PING,
                    payload=bytes(
                        [0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0xFF, 0x00, 0x00, 0x00]
                    ),
                )
            )
            # Mark connection healthy
            if not self.connection_success.done():
                self.connection_success.set_result(True)
        elif msg_type == P2PClientProtocolResponseMessageType.END:
            self.transport.close()
        elif msg_type == P2PClientProtocolResponseMessageType.PING:
            self.send(self.create_message(P2PClientProtocolRequestMessageType.PONG))
        elif msg_type == P2PClientProtocolResponseMessageType.ACK:
            num_acks = int.from_bytes(payload[4:6], byteorder="big")
            for i in range(num_acks):
                idx = 6 + (i * 2)
                seqno = int.from_bytes(payload[6 + (i * 2) : idx + 2], byteorder="big")
                # Acknowledge response for outstanding requests
                if seqno in self.pending:
                    self.pending[seqno].set()
        elif msg_type == P2PClientProtocolResponseMessageType.DATA:
            msg = payload[2:]
            seqno = msg[2] * 256 + msg[3]
            data_type = EufyP2PDataType(msg[0:2])
            self.acks[data_type].append(seqno)
            # Dedupe packets
            if seqno <= self.seen[data_type]:
                return
            self.seen[data_type] = seqno
            _LOGGER.debug(f"Processing {msg_type}:{data_type} with seq {seqno}")
            self.process_command(msg[8:])

    def process_command(self, payload: bytes):
        command_id = int.from_bytes(payload[0:2], "little")
        msg = payload[4:]
        try:
            command_type = CommandType(command_id)
            _LOGGER.debug(f"Received command type {command_type}")
            # Eufy protocol-level keepalive
            if command_type == CommandType.CMD_GET_DEVICE_PING and msg[6] == 0:
                _LOGGER.debug("Responding to device ping keepalive")
                self.wait_for(
                    self.async_send_command(
                        CommandType.CMD_GET_DEVICE_PING,
                        bytes([0x88, 0x00, 0x00, 0x00, 0x01] + [0] * 141),
                    )
                )
        except ValueError:
            _LOGGER.error(f"Received unknown command type: {command_id}")

    async def async_send_command(
        self, command_type: CommandType, payload: bytes = bytes()
    ):
        msg_seqno = self.seqno
        self.seqno += 1
        msg = bytearray(EufyP2PDataType.DATA.value)
        msg.extend(msg_seqno.to_bytes(2, byteorder="big"))
        msg.extend(b"XZYH")
        msg.extend(command_type.value.to_bytes(2, byteorder="little"))
        msg.extend(payload)
        _LOGGER.debug(f"Sending packet {command_type} ({len(msg)}): {msg}")
        self.send(self.create_message(P2PClientProtocolRequestMessageType.DATA, msg))
        self.pending[msg_seqno] = asyncio.Event()
        # Wait until the station has acked the request
        await self.pending[msg_seqno].wait()
        del self.pending[msg_seqno]

    def connection_lost(self, exc):
        if self.keepalive_task:
            self.keepalive_task.cancel()
        if not self.connection_success.done():
            _LOGGER.info("Connection closed")
            self.connection_success.set_result(False)


class P2PSession:
    """
    Implement the P2P protocol needed to talk to stations
    """

    def __init__(
        self, station_serial: str, p2p_did: str, discovery_key: str, actor: str
    ):
        self.station_serial = station_serial
        self.actor = actor
        self.p2p_did = p2p_did
        self.discovery_key = discovery_key
        self._session = None

    def valid_for(self, serial):
        return serial == self.station_serial

    async def connect(self, addr: str = None) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 0))
        loop = asyncio.get_running_loop()
        _, self.connection_manager = await loop.create_datagram_endpoint(
            lambda: ConnectionManager(), sock=sock,
        )

        candidates = await self.lookup(self.connection_manager, addr)
        local_addresses = [
            x for x in candidates if ipaddress.ip_address(x[0]).is_private
        ]
        remote_addresses = [x for x in candidates if x not in local_addresses]

        for candidate in local_addresses + remote_addresses:
            _LOGGER.info(f"Trying station address: {candidate}")
            connection_result = loop.create_future()
            handler = EufyP2PClientProtocol(loop, self.p2p_did, connection_result)
            self.connection_manager.connect(candidate, handler)
            if await connection_result is True:
                _LOGGER.info(f"Connected to {candidate}")
                self._session = handler
                return True
        return False

    async def close(self):
        if self._session:
            # Gracefully stop the connection and then forcibly close the transport
            self._session.close()
            self.connection_manager.close()

    async def lookup(
        self, connection_manager: ConnectionManager, addr: str
    ) -> List[Tuple[str, int]]:
        """
        Identifies the UDP ip+port combination needed to communicate with the station
        """
        if addr:
            _LOGGER.info(f"Trying discovery on {addr}")
            loop = asyncio.get_running_loop()
            discovery_result = loop.create_future()
            _, _ = await loop.create_datagram_endpoint(
                lambda: LocalDiscoveryP2PClientProtocol(loop, addr, discovery_result),
                local_addr=("0.0.0.0", 0),
            )
            return await discovery_result
        else:
            discovery_futures = []
            for seed in SEEDS:
                _LOGGER.info(f"Trying discovery seed {seed}")
                loop = asyncio.get_running_loop()
                discovery_result = loop.create_future()
                handler = DiscoveryP2PClientProtocol(
                    loop, self.p2p_did, self.discovery_key, discovery_result
                )
                connection_manager.connect((seed, 32100), handler)
                discovery_futures.append(discovery_result)

            discovery_results = await asyncio.gather(*discovery_futures)
            return list(
                set([item for sublist in discovery_results for item in sublist])
            )

    async def async_send_command_with_int_string(
        self, channel: int, command_type: CommandType, value: int
    ):
        """
        Advanced API method used to send requests that aren't exposed as convenience methods
        """
        payload = bytearray([0x88, 0x00])
        # I suspect this would be the place that specifies with channel/camera to act on but I don't have multiple devices to test
        payload.extend(
            [0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        )
        payload.extend([value] + [0] * 3)
        payload.extend(self.actor.encode())
        payload.extend([0] * 88)  # Unsure what this contains
        await self._session.async_send_command(command_type, payload=payload)

    async def async_send_command_with_int(
        self, channel: int, command_type: CommandType, value: int
    ):
        payload = bytearray([0x84, 0x00])
        payload.extend([0x00, 0x00, 0x01, 0x00, 0xFF, 0x00, 0x00, 0x00])
        payload.extend([value] + [0] * 3)
        payload.extend(self.actor.encode())
        payload.extend([0] * 88)
        await self._session.async_send_command(command_type, payload=payload)
