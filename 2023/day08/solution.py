from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import List, Optional


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


@dataclass
class Node:
    name: str
    l: Optional[Node] = None
    r: Optional[Node] = None


class Network:
    def __init__(self, text: str):
        self.instructions = text[0].strip().lower()
        self.start_node: Node = None
        self.ghost_start_nodes: List[Node] = []

        self._parse_nodes(text)

    def _parse_nodes(self, text: int) -> None:
        cache = {}

        for idx in range(2, len(text)):
            node, neighbors = text[idx].split(" = ")
            left, right = re.search(r"\(([A-Z]+), ([A-Z]+)\)", neighbors).groups()
            for n in (node, left, right):
                if n not in cache:
                    cache[n] = Node(n)
            cache[node].l = cache[left]
            cache[node].r = cache[right]
            if node == "AAA":
                self.start_node = cache[node]
            if node.endswith("A"):
                self.ghost_start_nodes.append(cache[node])

    def steps(self) -> int:
        step = 0
        current_node = self.start_node

        while current_node.name != "ZZZ":
            instruction = self.instructions[step%len(self.instructions)]
            current_node = getattr(current_node, instruction)
            step += 1

        return step

    @staticmethod
    def _all_nodes_end_with_z(nodes: List[Node]) -> bool:
        for node in nodes:
            if not node.name.endswith("Z"):
                return False
        return True

    def ghost_steps(self) -> int:
        step = 0
        current_nodes = self.ghost_start_nodes

        while not self._all_nodes_end_with_z(current_nodes):
            instruction = self.instructions[step%len(self.instructions)]
            new_nodes = []
            for node in current_nodes:
                new_nodes.append(getattr(node, instruction))
            current_nodes = new_nodes
            step += 1
            # print(f"{instruction} -> {[n.name for n in current_nodes]} {step}")

        return step


def s1(network: Network) -> int:
    return network.steps()


def s2(network: Network) -> int:
    return network.ghost_steps()


network = Network(text)
print(s1(network))
print(s2(network))
