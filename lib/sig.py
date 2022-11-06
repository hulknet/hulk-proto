from typing import Union

from secp256k1 import PublicKey


async def recovery(sig_rec_hex: str, body: bytes) -> Union[PublicKey, None]:
    """
    Recover the public key from a signature
    :param sig_rec_hex:
    :param body:
    :return:
    """
    empty = PublicKey()
    sig_rec_b_arr = bytearray.fromhex(sig_rec_hex)

    try:
        sig_rec = empty.ecdsa_recoverable_deserialize(bytes(sig_rec_b_arr[:64]), sig_rec_b_arr[64])
        pubkey = PublicKey(empty.ecdsa_recover(body, sig_rec))
    except Exception as e:
        return None

    return pubkey


async def verify_recoverable(session_pub_hex: str, sig_rec_hex: str, body: bytes) -> bool:
    """
    Verify a signature using the public key of the session
    :param session_pub_hex: Public key of the session
    :param sig_rec_hex: Signature to verify
    :param body: Body of the request
    :return:
    """
    if type(session_pub_hex) is bytes:
        session_pub_hex = session_pub_hex.decode()

    session_pub = await public_key_deserialize(session_pub_hex)
    req_pub = await recovery(sig_rec_hex, body)
    print(req_pub.serialize().hex())
    print(session_pub_hex)
    if req_pub.serialize().hex() != session_pub_hex:
        return False

    sig = await signature_deserialize(sig_rec_hex)
    if sig is None:
        return False

    return session_pub.ecdsa_verify(body, sig)


async def signature_deserialize(sig_rec_hex: str) -> Union[bytes, None]:
    """
    Deserialize a recoverable signature to regular signature
    :param sig_rec_hex:
    :return:
    """
    b_arr = bytearray.fromhex(sig_rec_hex)

    try:
        sig_rec = PublicKey().ecdsa_recoverable_deserialize(bytes(b_arr[:64]), b_arr[64])
        sig = PublicKey().ecdsa_recoverable_convert(sig_rec)
    except Exception as e:
        return None

    return sig


async def public_key_deserialize(pub_hex: str) -> Union[PublicKey, None]:
    """
    Deserialize a public key
    :param pub_hex:
    :return:
    """
    try:
        pub = PublicKey(bytes(bytearray.fromhex(pub_hex)), raw=True)
    except Exception as e:
        return None

    return pub
