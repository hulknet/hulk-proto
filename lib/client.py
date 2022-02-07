import asyncio
from enum import IntEnum


class Ports(IntEnum):
    """
    Ports for the server.
    """
    instruction = 8001
    storage = 8005
    memory = 8006
    cpu = 8007


async def instruction_client(message: bytes):
    await tcp_client('instruction', message)


async def storage_client(message: bytes):
    await tcp_client('storage', message)


async def memory_client(message: bytes):
    await tcp_client('memory', message)


async def cpu_client(message: bytes):
    await tcp_client('cpu', message)


async def tcp_client(app: str, message: bytes):
    reader, writer = await asyncio.open_connection('127.0.0.1', Ports[app].value)

    writer.write(message)
    await writer.drain()

    data = await reader.read(1)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()
