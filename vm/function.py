from attrs import define

from lib.id import ID8


@define
class Function:
    id: ID8
    code: List[bytes]
    vm_id: int
