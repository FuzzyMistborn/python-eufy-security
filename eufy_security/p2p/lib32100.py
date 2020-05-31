import math

from .types import (
    P2PClientProtocolRequestMessageType,
    P2PClientProtocolResponseMessageType,
)


class BaseP2PClientProtocol:
    def create_message(
        self, msg_type: P2PClientProtocolRequestMessageType, payload=bytearray()
    ):
        msg = bytearray()
        msg.extend(msg_type.value)
        payload_size = len(payload)
        msg.append(math.floor(payload_size / 256))
        msg.append(payload_size % 256)
        msg.extend(payload)
        return msg

    def datagram_received(self, data, _):
        msg_type = P2PClientProtocolResponseMessageType(bytes(data[0:2]))
        payload = data[2:]
        self.process_response(msg_type, payload)

    def process_response(
        self, msg_type: P2PClientProtocolResponseMessageType, payload: bytes
    ):
        raise NotImplementedError()
