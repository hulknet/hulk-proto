import asyncio
import secrets
from functools import reduce

from lib.client import instruction_client
from lib.types import RequestType, Driver


def init(subparsers):
    announce_parser = subparsers.add_parser('announce', help='Announce a message')
    announce_parser.set_defaults(func=handle_announce)
    announce_parser.add_argument('driver', type=str, choices=['store', 'memory', 'cpu'], default='memory')
    announce_parser.add_argument('command', type=str, default='get')
    announce_parser.add_argument('-i', '--input', nargs='+', type=lambda x: bytes.fromhex(x))
    announce_parser.add_argument('-o', '--output', nargs='+', type=lambda x: bytes.fromhex(x))
    announce_parser.add_argument('-d', '--data', type=lambda x: bytes.fromhex(x), default=b'')

    input_parser = subparsers.add_parser('input', help='Input a message')
    input_parser.set_defaults(func=handle_input)
    input_parser.add_argument('id', type=lambda x: bytes.fromhex(x))
    input_parser.add_argument('-d', '--data', type=lambda x: bytes.fromhex(x), default=b'')


def handle_announce(args):
    req = RequestType['announce'].bytes()
    header = bytes.fromhex(secrets.token_hex(8))
    header += Driver[args.driver].bytes_with_command(args.command)
    header += len(args.input).to_bytes(1, "big") + reduce(lambda a, b: a + b, args.input)
    header += int(0).to_bytes(1, "big")  # output count
    req += len(header).to_bytes(2, "big") + header
    req += len(args.data).to_bytes(4, "big") + args.data
    print(req.hex())
    asyncio.run(instruction_client(req))


def handle_input(args):
    req = RequestType['input'].bytes()
    req += args.id
    req += len(args.data).to_bytes(4, "big") + args.data
    asyncio.run(instruction_client(req))
