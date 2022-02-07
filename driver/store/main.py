import asyncio


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print(reader.readline())
    pass


async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 8005)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
