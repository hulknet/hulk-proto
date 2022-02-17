from functools import reduce
from typing import List, Dict

from lib.types import ID8, ID8Partition, EnumIntDefault, lenb
from request import AnnounceRequest


class Instruction:
    def __init__(self, req: AnnounceRequest):
        self.id: ID8 = req.id
        self.driver: EnumIntDefault = req.driver
        self.command: EnumIntDefault = req.command
        self.input_ids: List[ID8Partition] = req.inputs
        self.output_ids: List[ID8Partition] = req.outputs
        self.input_parts: Dict[ID8, bytes] = {}

    def add_input_part(self, input_part_id: ID8, value: bytes):
        self.input_parts[input_part_id] = value

    def is_ready(self) -> bool:
        return len(self.input_parts) == reduce(lambda r, x: r + len(x), self.input_ids, 0)  # weak check

    def encode(self) -> bytes:
        e = self.command.bytes()
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
