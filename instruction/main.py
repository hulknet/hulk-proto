import asyncio
from typing import Dict

from instruction import Instruction
from lib.types import RequestType, int_from_async_reader, ID8
from request import AnnounceRequest, InputRequest

instructions: Dict[ID8, Instruction] = dict()
input_values: Dict[ID8, bytes] = dict()
input_to_instruction: Dict[ID8, ID8] = dict()


async def handle_announce_request(req: AnnounceRequest):
    if req.id in instructions:
        print(f"Instruction {req.id} already exists")
        return

    instructions[req.id] = Instruction(req)
    print(f"Instruction added: {req.id.hex()}")
    for input_parts in instructions[req.id].input_ids:
        for input_id in input_parts:
            if input_id in input_values:
                instructions[req.id].input_parts[input_id] = input_values[input_id]
                del input_values[input_id]
                print(f"Input value added: {input_id.hex()} to {req.id.hex()}")
            else:
                input_to_instruction[input_id] = req.id
                print(f"Input id waiting: {input_id.hex()}")

    if instructions[req.id].is_ready():
        pass


async def handle_input_request(req: InputRequest):
    if req.id in input_to_instruction:
        instruction_id = input_to_instruction[req.id]
        instructions[instruction_id].add_input_part(req.id, req.data)
        del input_to_instruction[req.id]
        print(f"Input value added: {req.id.hex()} to {instruction_id.hex()}")

        if instructions[instruction_id].is_ready():
            pass
    else:
        input_values[req.id] = req.data
        print(f"Input value waiting: {req.id.hex()}")


async def handle(reader, writer):
    try:
        req_type = RequestType(await int_from_async_reader(reader, 1))
        if req_type == RequestType.announce:
            await handle_announce_request(await AnnounceRequest.read(reader))
        elif req_type == RequestType.input:
            await handle_input_request(await InputRequest.read(reader))
        else:
            print("Unknown request type")
    except Exception as e:
        print("Error:", e)
    finally:
        writer.close()


async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 8001)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
