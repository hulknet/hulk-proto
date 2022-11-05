from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json
from secp256k1 import PrivateKey, PublicKey

from config.secrets import private_key

bp_service = Blueprint("service", url_prefix="/service")


@bp_service.post('/sign')
async def sign(request: Request):
    privkey = PrivateKey(bytes(private_key), raw=True)
    # sig = privkey.ecdsa_sign(request.body)
    # verified = privkey.pubkey.ecdsa_verify(request.body, sig)

    sig = privkey.ecdsa_sign_recoverable(request.body)
    sig_ser, index = privkey.ecdsa_recoverable_serialize(sig)
    sig_arr = bytearray(sig_ser)
    sig_arr.append(index)

    return json({
        'signature': sig_arr.hex(),
        'message': request.body.decode(),
    })


@bp_service.post('/verify')
async def verify(request: Request):
    empty = PublicKey()
    sig_hex = request.headers.get('X-Authorization')
    b_arr = bytearray.fromhex(sig_hex)
    sig_rec = empty.ecdsa_recoverable_deserialize(bytes(b_arr[:64]), b_arr[64])
    pubkey = PublicKey(empty.ecdsa_recover(request.body, sig_rec))
    sig = empty.ecdsa_recoverable_convert(sig_rec)
    verified = pubkey.ecdsa_verify(request.body, sig)

    return json({'valid': verified, 'key': pubkey.serialize().hex()})
