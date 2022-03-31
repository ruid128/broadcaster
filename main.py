import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from environs import Env
from server import Server
from utils import get_current_pc_ip_port, start_zmq_connection, BadInput
import logging

logging.basicConfig(filename='broadcaster.log',
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO)

env = Env()
env.read_env()


async def main():
    IP, PORT = env("SERVER_ADDRESS").split(':')
    ZMQ_ADDRESS = env('ZMQ_ADDRESS')

    server = Server(IP, PORT)
    message_queue = server.message_bus
    zmq_task = start_zmq_connection(ZMQ_ADDRESS, message_queue)
    serv_task = server.run()
    print(f"Sub task started on {ZMQ_ADDRESS}")
    print(f'Broadcast task started on {IP}:{PORT}')
    await asyncio.gather(serv_task, zmq_task)


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        print('CUM')
