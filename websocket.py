import asyncio
import typing

from websockets import serve
from websockets.exceptions import ConnectionClosedOK


class Websocket:

    def __init__(self, on_message: typing.Callable[[str], None]):
        self.host = "localhost"
        self.port = 7890
        self.connection_set = set()
        self.onMessage = on_message

    async def socketHandler(self, socket):
        self.connection_set.add(socket)
        print("connection established")
        try:
            while True:
                message = await socket.recv()
                self.onMessage(message)
        except ConnectionClosedOK:
            self.connection_set.remove(socket)
            print("connection closed")

    async def startServer(self):
        print(f"starting ws server on {self.host}-{self.port}")
        async with serve(self.socketHandler, self.host, self.port):
            await asyncio.Future()
