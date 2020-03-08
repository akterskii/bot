import json
from typing import List, Set

from main_logic.quest_node import Node


def verify_graph(nodes: List[Node]):
    ids: Set[int] = set()
    for node in nodes:
        ids.add(node.get_id())

    for node in nodes:
        if not ids.issuperset(node.get_next_node_ids()):
            return False
    return True


def parse_file(input_file_name: str) -> List[Node]:
    nodes: List[Node] = []
    with open(input_file_name, 'r') as input_file:
        json_data = json.load(input_file)
        for elem in json_data:
            nodes.append(Node.from_dict(elem))
    return nodes