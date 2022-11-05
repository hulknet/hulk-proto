import asyncio

from redis import asyncio as aioredis

from config.config import (
    net_id,
    node_id,
)
from config.secrets import (
    pubkey,
)

prefix = net_id + b":" + node_id + b":"


async def main():
    redis = aioredis.from_url("redis://localhost:6380/0")
    await redis.sadd(prefix + b"known_keys", bytes(pubkey))
    print(pubkey)
    value = await redis.sismember(prefix + b"known_keys", bytes(pubkey))
    print(value)
    value = await redis.smembers(prefix + b"known_keys")
    print(value)


if __name__ == "__main__":
    asyncio.run(main())
