import asyncio

from .lib32100 import BaseP2PClientProtocol
from .types import (
    P2PClientProtocolRequestMessageType,
    P2PClientProtocolResponseMessageType,
)


class DiscoveryP2PClientProtocol(BaseP2PClientProtocol):
    def __init__(self, loop, p2p_did: str, key: str, on_conn_lost):
        self.loop = loop
        self.p2p_did = p2p_did
        self.key = key
        self.on_conn_lost = on_conn_lost
        self.addresses = []
        self.response_count = 0

    def connection_made(self, transport, addr):
        # Build payload
        p2p_did_components = self.p2p_did.split("-")
        payload = bytearray(p2p_did_components[0].encode())
        payload.extend(int(p2p_did_components[1]).to_bytes(5, byteorder="big"))
        payload.extend(p2p_did_components[2].encode())
        payload.extend([0x00, 0x00, 0x00, 0x00, 0x00])
        ip, port = transport.get_extra_info("sockname")
        payload.extend(port.to_bytes(2, byteorder="little"))
        payload.extend([int(x) for x in ip.split(".")[::-1]])
        payload.extend(
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x04, 0x00, 0x00]
        )
        payload.extend(self.key.encode())
        payload.extend([0x00, 0x00, 0x00, 0x00])

        transport.sendto(
            self.create_message(
                P2PClientProtocolRequestMessageType.LOOKUP_WITH_KEY, payload
            ),
            addr,
        )
        # Manually timeout if we don't get an answer
        self.loop.create_task(self.timeout(1.5))

    async def timeout(self, seconds: float):
        await asyncio.sleep(seconds)
        self.return_candidates()

    def process_response(
        self, msg_type: P2PClientProtocolResponseMessageType, payload: bytes
    ):
        msg = payload[2:]
        if msg_type == P2PClientProtocolResponseMessageType.LOOKUP_ADDR:
            port = payload[5] * 256 + payload[4]
            ip = f"{payload[9]}.{payload[8]}.{payload[7]}.{payload[6]}"
            self.addresses.append((ip, port))

            # We expect at most two IP/port combos so we can bail early
            # if we received both
            self.response_count += 1
            if self.response_count == 2:
                self.return_candidates()

    def error_received(self, exc):
        _LOGGER.exception("Error received", exc_info=exc)

    def return_candidates(self):
        if not self.on_conn_lost.done():
            self.on_conn_lost.set_result(self.addresses)
