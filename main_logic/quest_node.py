from typing import NamedTuple, List, Set

from main_logic.id_generator import IdGenerator


class Reply(NamedTuple):
    text: str
    next_id: int


class Node:
    def __init__(self):
        self.id = IdGenerator.next_id()
        self.text = ''
        self.hints:List[str] = []
        self.replies: List[Reply] = []


    def get_id(self) -> int:
        return self.id

    def get_next_node_ids(self) -> Set[int]:
        ids = set()
        for reply in self.replies:
            ids.add(reply.next_id)
        return ids
