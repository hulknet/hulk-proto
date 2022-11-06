import secrets

from sanic import Blueprint, Request, json

from lib.sig import recovery

bp_auth = Blueprint("auth", url_prefix="/auth")


@bp_auth.get("/key")
async def generate_key(request: Request):
    new_key = secrets.token_hex(8)
    await request.app.ctx.db.sadd(request.app.ctx.prefix + f"auth:key", new_key)
    return json({"key": new_key})


@bp_auth.post("/login")
async def login(request: Request):
    key = request.body
    if not key:
        return json({"error": "No key provided"}, status=400)
    if not await request.app.ctx.db.sismember(request.app.ctx.prefix + f"auth:key", key):
        return json({"error": "Invalid key"}, status=401)
    await request.app.ctx.db.srem(request.app.ctx.prefix + f"auth:key", key)

    sig = request.headers.get("signature")
    if not sig:
        return json({"error": "No signature provided"}, status=400)

    pubkey = await recovery(sig, request.body)
    if not pubkey:
        return json({"error": "Invalid signature"}, status=401)

    if not await request.app.ctx.db.execute_command(
            "BF.EXISTS", request.app.ctx.prefix + f"known_keys", pubkey.serialize().hex()):
        return json({"error": "Unknown public key"}, status=401)

    session_key = secrets.token_hex(32)
    await request.app.ctx.db.hset(request.app.ctx.prefix + f"auth:session", session_key, pubkey.serialize().hex())

    return json({"session": session_key})
