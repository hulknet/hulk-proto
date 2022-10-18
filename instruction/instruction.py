import asyncio
from io import BytesIO
from typing import List, Dict

from attr import define, field

from lib.types import ID8, Driver, lenb, int_from_async_reader, int_from_buffer


@define
class Instruction:
    id: ID8
    driver: Driver
    command_id: int
    input_ids: List[ID8]
    output_ids: List[ID8]
    input_data: Dict[ID8, bytes] = field(default={})

    def add_input(self, input_id: ID8, value: bytes):
        self.input_data[input_id] = value

    def is_ready(self) -> bool:
        return len(self.input_data) == len(self.input_ids)

    # | command_id | input_parts | output_ids |
    def encode(self) -> bytes:
        e = self.driver.command(self.command_id).bytes()
        e += lenb(self.input_ids, 1)
        for input_id in self.input_ids:
            d = bytes()
            d += self.input_data[input_id]
            e += lenb(d, 4)
            e += d

        e += lenb(self.output_ids, 1)
        for parts in self.output_ids:
            e += lenb(parts, 1)
            for part_id in parts:
                e += part_id

        return e


async def read_instruction_announce(reader: asyncio.StreamReader) -> 'Instruction':
    header_len = await int_from_async_reader(reader, 2)
    buf = BytesIO(await reader.readexactly(header_len))

    def read_ids(b: BytesIO) -> List[ID8]:
        return [ID8(b.read(8)) for _ in range(int_from_buffer(b, 1))]

    return Instruction(
        id=ID8(buf.read(8)),
        driver=Driver(int_from_buffer(buf, 1)),
        command_id=int_from_buffer(buf, 1),
        input_ids=read_ids(buf),
        output_ids=read_ids(buf),
    )


@define
class Input:
    id: ID8
    data: bytes


async def read_instruction_input(reader: asyncio.StreamReader) -> 'Input':
    return Input(id=ID8(await reader.readexactly(8)),
                 data=await reader.readexactly(await int_from_async_reader(reader, 4)))
