from secp256k1 import PublicKey


def init(subparsers):
    parser = subparsers.add_parser('recovery', help='Recover public key from signature')
    parser.add_argument('signature', help='Signature')
    parser.add_argument('msg', help='Message')
    parser.set_defaults(func=recovery)


def recovery(args):
    empty = PublicKey()
    b_arr = bytearray.fromhex(args.signature)

    print(bin(int(args.signature, 16))[2:])
    print(len(bin(int(args.signature, 16))[2:]))

    sig = empty.ecdsa_recoverable_deserialize(bytes(b_arr[:64]), b_arr[64])
    pubkey = empty.ecdsa_recover(bytearray.fromhex(args.msg), sig)

    print("Public Key: {}".format(PublicKey(pubkey).serialize().hex()))
