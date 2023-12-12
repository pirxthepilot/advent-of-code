from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Optional


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
    
    def steps(self) -> int:
        step = 0
        current_node = self.start_node

        while current_node.name != "ZZZ":
            instruction = self.instructions[step%len(self.instructions)]
            current_node = getattr(current_node, instruction)

            step += 1
        
        return step


def s1(network: Network) -> int:
    return network.steps()


network = Network(text)
print(s1(network))
