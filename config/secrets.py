from secp256k1 import PrivateKey

private_key = bytearray.fromhex("11bdb63af68b58c51c8c32e1981de86597f943ec8d8a8c8e9776ec8819414c30")
privkey = PrivateKey(bytes(private_key), raw=True)
pubkey = privkey.pubkey.serialize()
