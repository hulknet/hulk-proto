import asyncio
from enum import IntEnum


class EnumIntDefault(IntEnum):
    @classmethod
    def _missing_(cls, value):
        return -1

    def bytes(self) -> bytes:
        return self.to_bytes(1, 'big')


class RequestType(EnumIntDefault):
    announce = 0
    input = 1


class Driver(EnumIntDefault):
    store = 0
    memory = 1
    cpu = 2

    def command(self, command_id: int) -> 'Command':
        match self:
            case Driver.store:
                return StoreCommand(command_id)
            case Driver.memory:
                return MemoryCommand(command_id)
            case Driver.cpu:
                return CpuCommand(command_id)
            case -1:
                raise ValueError(f'Unknown driver: {self}')

    def bytes_with_command(self, name: str) -> bytes:
        command_bytes = bytes()

        match self:
            case Driver.store:
                command_bytes = StoreCommand[name].bytes()
            case Driver.memory:
                command_bytes = MemoryCommand[name].bytes()
            case Driver.cpu:
                command_bytes = CpuCommand[name].bytes()
            case -1:
                raise ValueError(f'Unknown driver: {self}')

        return self.bytes() + command_bytes


Command = EnumIntDefault


class StoreCommand(Command):
    get = 0
    set = 1


class MemoryCommand(Command):
    get = 0
    set = 1


class CpuCommand(Command):
    sum = 0
    mult = 1


# ID types
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


async def int_from_async_reader(reader: asyncio.StreamReader, size: int = 8) -> int:
    return int.from_bytes(await reader.readexactly(size), byteorder='big')
