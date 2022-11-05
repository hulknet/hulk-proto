from sanic import Blueprint
from sanic import Request

bp_user = Blueprint("user", url_prefix="/user")


@bp_user.on_request
async def check_pub(req: Request):
    req.headers.get("Pub")
    pass
