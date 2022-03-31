import asyncio
import websockets
from os import system


class Server:

    __slots__ = 'ip', 'port', 'message_bus', 'online_clients'

    def __init__(self, ip: str, port: int, message_bus: asyncio.Queue = None):
        self.ip = ip
        self.port = port
        self.message_bus = message_bus or asyncio.Queue()
        self.online_clients = set()


    def print_status(self):
        system('cls')
        print(f'Online clients: {len(self.online_clients)}')

    def add_client(self, websocket):
        self.online_clients.add(websocket)
        self.print_status()

    def remove_client(self, websocket):
        self.online_clients.remove(websocket)
        self.print_status()

    async def hello(self, websocket):
        self.add_client(websocket)
        await websocket.wait_closed()
        self.remove_client(websocket)

    async def broadcast_messages(self):
        while 1:
            message = await self.message_bus.get()
            self.message_bus.task_done()
            websockets.broadcast(self.online_clients, message)

    async def run(self):
        async with websockets.serve(self.hello, self.ip, self.port):
            await self.broadcast_messages()