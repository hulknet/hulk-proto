from . import (
    pk_recovery,
    pk_sing,
    msg
)


def init(subparsers):
    pk_recovery.init(subparsers)
    pk_sing.init(subparsers)
    msg.init(subparsers)
