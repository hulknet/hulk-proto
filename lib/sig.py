from typing import Union

from secp256k1 import PublicKey


async def recovery(sig: str, body: bytes) -> Union[PublicKey, None]:
    empty = PublicKey()
    b_arr = bytearray.fromhex(sig)

    # try:

    sig_rec = empty.ecdsa_recoverable_deserialize(bytes(b_arr[:64]), b_arr[64])
    pubkey = PublicKey(empty.ecdsa_recover(body, sig_rec))
    # except Exception as e:
    #     return None

    return pubkey
