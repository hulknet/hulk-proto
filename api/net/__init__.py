from sanic import Blueprint, json
from sanic import Request

from lib.sig import verify_recoverable

bp_net = Blueprint("net", url_prefix="/net")


@bp_net.on_request()
async def authentication(request: Request):
    if not request.headers.get("session"):
        return json({"error": "No session provided"}, status=400)

    if not request.headers.get("signature"):
        return json({"error": "No signature provided"}, status=400)

    session_pub_hex = await request.app.ctx.db.hget(request.app.ctx.prefix + f"auth:session",
                                                    request.headers.get("session"))
    if not session_pub_hex:
        return json({"error": "Invalid session"}, status=401)

    if not await verify_recoverable(session_pub_hex, request.headers.get("signature"), request.body):
        return json({"error": "Invalid signature"}, status=401)

    request.ctx.public_key = session_pub_hex


@bp_net.post("/echo")
async def echo(request: Request):
    return json({"body": request.body.decode()})
