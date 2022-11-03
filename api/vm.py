from attrs import define
from cattrs.preconf.json import make_converter
from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json

converter = make_converter()
bp_vm = Blueprint("vm", url_prefix="/vm")


@define
class VM:
    id: int
    name: str


@bp_vm.post('/ask')
async def ask(request: Request):
    return json({'message': 'hello'})
