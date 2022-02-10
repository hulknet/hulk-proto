import asyncio
from io import BytesIO
from typing import List, Optional

from lib.types import (
    ID8, ID8Partition,
    int_from_async_reader, int_from_buffer, Driver, Command)


class AnnounceRequest:
    def __init__(self):
        self.id: Optional[ID8] = None
        self.driver: Optional[Driver] = None
        self.command: Optional[Command] = None
        self.inputs: List[ID8Partition] = list()
        self.outputs: List[ID8Partition] = list()
        self.data: bytes

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> 'AnnounceRequest':
        header_len = await int_from_async_reader(reader, 2)
        buf = BytesIO(await reader.readexactly(header_len))

        req = AnnounceRequest()
        req.id = ID8(buf.read(8))
        req.driver = Driver(int.from_bytes(buf.read(1), 'big'))
        req.command = req.driver.command(int.from_bytes(buf.read(1), 'big'))

        def read_partition(b: BytesIO) -> ID8Partition:
            return [ID8(b.read(8)) for _ in range(int_from_buffer(b, 1))]

        req.inputs = [read_partition(buf) for _ in range(int_from_buffer(buf, 1))]
        req.outputs = [read_partition(buf) for _ in range(int_from_buffer(buf, 1))]

        data_len = await int_from_async_reader(reader, 4)
        req.data = await reader.readexactly(data_len)

        return req


class InputRequest(object):
    def __init__(self):
        self.id: Optional[ID8] = None
        self.data: Optional[bytes] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> 'InputRequest':
        req = InputRequest()
        req.id = ID8(await reader.readexactly(8))

        data_len = await int_from_async_reader(reader, 4)
        req.data = await reader.readexactly(data_len)

        return req
