import asyncio
import logging
from typing import Dict

from instruction import Instruction, read_instruction_announce, read_instruction_input
from lib.client import cpu_client, memory_client, storage_client
from lib.types import RequestType, int_from_async_reader, ID8, Driver

instructions: Dict[ID8, Instruction] = dict()
input_values: Dict[ID8, bytes] = dict()
input_to_instruction: Dict[ID8, ID8] = dict()


async def send_instruction(instruction: Instruction):
    match instruction.driver:
        case Driver.cpu:
            await cpu_client(instruction.encode())
        case Driver.store:
            await storage_client(instruction.encode())
        case Driver.memory:
            await memory_client(instruction.encode())


async def handle_announce_request(reader: asyncio.StreamReader):
    inst = await read_instruction_announce(reader)
    if inst.id in instructions:
        logging.info(f"Instruction {inst.id} already exists")
        return

    instructions[inst.id] = inst
    logging.info(f"Instruction added: {inst.id.hex()}")
    for input_parts in instructions[inst.id].input_ids:
        for input_id in input_parts:
            if input_id in input_values:
                instructions[inst.id].add_input_part(input_id, input_values[input_id])
                del input_values[input_id]
                logging.info(f"Input value added: {input_id.hex()} to {inst.id.hex()}")
            else:
                input_to_instruction[input_id] = inst.id
                logging.info(f"Input id waiting: {input_id.hex()}")

    if instructions[inst.id].is_ready():
        logging.info(f"Instruction {inst.id.hex()} is ready: {instructions[inst.id].encode().hex()}")
        await send_instruction(instructions[inst.id])


async def handle_input_request(reader: asyncio.StreamReader):
    i = await read_instruction_input(reader)
    if i.id in input_to_instruction:
        instruction_id = input_to_instruction[i.id]
        instructions[instruction_id].add_input_part(i.id, i.data)
        del input_to_instruction[i.id]
        logging.info(f"Input value added: {i.id.hex()} to {instruction_id.hex()}")

        if instructions[instruction_id].is_ready():
            logging.info(f"Instruction {instruction_id.hex()} is ready: {instructions[instruction_id].encode().hex()}")
            await send_instruction(instructions[instruction_id])
    else:
        input_values[i.id] = i.data
        logging.info(f"Input value waiting: {i.id.hex()}")


async def handle(reader, writer):
    try:
        req_type = RequestType(await int_from_async_reader(reader, 1))
        if req_type == RequestType.announce:
            await handle_announce_request(reader)
        elif req_type == RequestType.input:
            await handle_input_request(reader)
        else:
            logging.info("Unknown request type")
    except Exception as e:
        logging.error("Error:", e)
    finally:
        writer.close()


async def main():
    logging.basicConfig(level=logging.INFO)

    server = await asyncio.start_server(handle, '127.0.0.1', 8001)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
