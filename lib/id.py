from typing import Sized


class Instruction(bytes):
    def __init__(self, value: bytes):
        if len(value) != 4:
            raise ValueError(f'Instruction must be 4 bytes, not {len(value)}')

    def __repr__(self):
        return f'Instruction({super().__repr__()})'


class ID8(bytes):
    def __new__(cls, value):
        if len(value) != 8:
            raise ValueError("ID8 must be 8 bytes long")
        return super().__new__(cls, value)


class ID32(bytes):
    def __new__(cls, value):
        if len(value) != 32:
            raise ValueError("ID32 must be 32 bytes long")
        return super().__new__(cls, value)


# helpers
def int_from_buffer(buf, size: int = 8) -> int:
    return int.from_bytes(buf.read(size), byteorder='big')


def lenb(iterable: Sized, size: int) -> bytes:
    return len(iterable).to_bytes(size, byteorder='big')
