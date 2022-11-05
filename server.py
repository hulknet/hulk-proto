from redis import asyncio as aioredis
from sanic import Sanic
from secp256k1 import PrivateKey

from api.auth import bp_auth
from api.net import bp_net
from api.service import bp_service
from api.user import bp_user

app = Sanic("hulk")
app.update_config('config/config.py')

app.blueprint([bp_service, bp_auth, bp_net, bp_user])


@app.listener("before_server_start")
async def setup(a):
    a.ctx.db = await aioredis.from_url(f"redis://{a.config.REDIS_HOST}:{a.config.REDIS_PORT}/{a.config.REDIS_DB}")
    a.ctx.prefix = f"{a.config.NET}:{a.config.NODE}:{a.config.TIME}:"
    a.ctx.private_key = PrivateKey(bytes(bytearray.fromhex(a.config.PRIVATE_KEY)), raw=True)
    a.ctx.public_key = a.ctx.private_key.pubkey


if __name__ == '__main__':
    app.run()
