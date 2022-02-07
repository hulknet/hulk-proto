from typing import Set, Dict

from lib.types import ID8, EnumIntDefault
from request import AnnounceRequest


class Instruction:
    def __init__(self, req: AnnounceRequest):
        self.id: ID8 = req.id
        self.driver: EnumIntDefault = req.driver
        self.command: EnumIntDefault = req.command
        self.input_ids: Set[ID8] = req.inputs
        self.output_ids: Set[ID8] = req.outputs
        self.inputs: Dict[ID8, bytes] = {}

    def set_input(self, input_id: ID8, value: bytes):
        self.inputs[input_id] = value

    def is_ready(self) -> bool:
        return len(self.inputs) == len(self.input_ids)
