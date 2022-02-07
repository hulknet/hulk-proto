import asyncio

from aiohttp import web


async def proxy(req: web.Request):
    t = await req.read()

    reader, writer = await asyncio.open_connection('127.0.0.1', 8001)
    writer.write(bytes.fromhex(t.decode()))
    writer.close()

    return web.Response(status=200)


async def init():
    app = web.Application()
    app.router.add_post("/", proxy)
    return app


if __name__ == "__main__":
    application = init()
    web.run_app(application, port=8000)
