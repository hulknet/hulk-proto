import os

from secp256k1 import PrivateKey


def sign(args):
    p_key = PrivateKey(bytes(bytearray.fromhex(args.private_key)), raw=True)
    s = p_key.ecdsa_sign_recoverable(bytearray.fromhex(args.msg))
    s_ser, index = p_key.ecdsa_recoverable_serialize(s)
    b_arr = bytearray(s_ser)
    b_arr.append(index)

    print("Signature: {}".format(b_arr.hex()))


def init(subparsers):
    hello_parser = subparsers.add_parser('sign')
    hello_parser.set_defaults(func=sign)
    hello_parser.add_argument('msg')
    hello_parser.add_argument('--private-key', default=os.environ.get('HULK_PRIVATE_KEY'), help='private key')
