import asyncio


class ConnectionManager(asyncio.DatagramProtocol):
    def __init__(self):
        self.connection_map = {}

    def connect(self, target, protocol):
        self.connection_map[target] = protocol
        protocol.connection_made(self.transport, target)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if addr in self.connection_map:
            self.connection_map[addr].datagram_received(data, addr)

    def connection_lost(self, exc):
        for _, protocol in self.connection_map.items():
            protocol.connection_lost(exc)

    def close(self):
        self.transport.close()
