import asyncio
from functools import reduce
from io import BytesIO
from typing import List, Dict

from attr import define, field

from lib.types import ID8, ID8Partition, Driver, lenb, int_from_async_reader, int_from_buffer


@define
class Instruction:
    id: ID8
    driver: Driver
    command_id: int
    input_ids: List[ID8Partition]
    output_ids: List[ID8Partition]
    input_parts: Dict[ID8, bytes] = field(default={})

    def add_input_part(self, input_part_id: ID8, value: bytes):
        self.input_parts[input_part_id] = value

    def is_ready(self) -> bool:
        return len(self.input_parts) == reduce(lambda r, x: r + len(x), self.input_ids, 0)  # weak check

    def encode(self) -> bytes:
        e = self.driver.command(self.command_id).bytes()
        e += lenb(self.input_ids, 1)
        for parts in self.input_ids:
            d = bytes()
            for part_id in parts:
                d += self.input_parts[part_id]  # TODO: implement data merging
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

    def read_partition(b: BytesIO) -> ID8Partition:
        return [ID8(b.read(8)) for _ in range(int_from_buffer(b, 1))]

    return Instruction(
        id=ID8(buf.read(8)),
        driver=Driver(int_from_buffer(buf, 1)),
        command=int_from_buffer(buf, 1),
        input_ids=read_partition(buf),
        output_ids=read_partition(buf),
    )


@define
class Input:
    id: ID8
    data: bytes


async def read_instruction_input(reader: asyncio.StreamReader) -> 'Input':
    return Input(id=ID8(await reader.readexactly(8)),
                 data=await reader.readexactly(await int_from_async_reader(reader, 4)))
