import asyncio

from lib.types import ID8

store = dict[ID8, bytes]


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    command_id = await reader.readexactly(1)
    if command_id == b'\x00':
        await handle_get(reader, writer)
    if command_id == b'\x01':
        await handle_set(reader, writer)
    pass


async def handle_get(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    key_len = await reader.readexactly(1)
    key = await reader.readexactly(key_len)
    value = await reader.readexactly(1)
    writer.write(value)
    await writer.drain()
    writer.close()


async def handle_set(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    key_len = await reader.readexactly(1)
    key = await reader.readexactly(key_len)
    value_len = await reader.readexactly(1)
    value = await reader.readexactly(value_len)
    writer.write(b'\x00')
    await writer.drain()
    writer.close()


async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 8005)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
