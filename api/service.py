from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json
from secp256k1 import PrivateKey

from config.secrets import private_key

bp_service = Blueprint("service", url_prefix="/service")


@bp_service.post('/sign')
async def sign(request: Request):
    privkey = PrivateKey(bytes(private_key), raw=True)
    sig = privkey.ecdsa_sign(request.body)

    verified = privkey.pubkey.ecdsa_verify(request.body, sig)

    return json({
        'signature': privkey.ecdsa_serialize(sig).hex(),
        'message': request.json
    })


@bp_service.post('/verify')
async def verify(request: Request):
    privkey = PrivateKey(bytes(private_key), raw=True)

    sig_hex = request.headers.get('X-Authorization')
    sig = privkey.ecdsa_deserialize(bytes(bytearray.fromhex(sig_hex)))
    verified = privkey.pubkey.ecdsa_verify(request.body, sig)

    return json({'valid': verified})
