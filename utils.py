import asyncio
import os
import sys

from zmq.asyncio import Context
import zmq


async def start_zmq_connection(pub_address: str, message_queue: asyncio.Queue):
    ctx = Context()
    socket = ctx.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '0')
    socket.connect(pub_address)
    while 1:
        channel, data = (await socket.recv_string()).split()
        await message_queue.put(data)
    socket.close()


def get_current_pc_ip_port() -> (str, int):
    IP = os.getenv('IP')
    PORT = os.getenv('PORT')

    if not (IP and PORT):

        try:
            IP, PORT = sys.argv[1].split(':')
        except (IndexError, ValueError):
            raise BadInput('IP:PORT incorrect')

    return IP, int(PORT)


class BadInput(Exception):
    pass