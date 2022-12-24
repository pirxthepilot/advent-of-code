from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import List, Optional
from uuid import uuid4


@dataclass
class Cipher:
    value: int
    right: Optional[Cipher] = None
    left: Optional[Cipher] = None

    def __post_init__(self):
        self.uuid = uuid4()

    def __repr__(self):
        return f"Cipher({self.value})"
    
    def __hash__(self) -> int:
        return hash(self.uuid)


class Encrypted:
    def __init__(self, ciphers: List[Cipher]):
        self.ciphers = ciphers
        self.pointers = [c.uuid for c in self.ciphers]
    
    @classmethod
    def link(cls, l: Cipher, r: Cipher) -> None:
        l.right = r
        r.left = l
    
    @classmethod
    def unlink(cls, c: Cipher) -> None:
        """ Remove from chain """
        c.left.right = c.right
        c.right.left = c.left
        c.left = None
        c.right = None
    
    @classmethod
    def insert(cls, c: Cipher, l: Cipher, r: Cipher) -> None:
        cls.link(l, c)
        cls.link(c, r)
    
    def _find_cipher(self, uuid) -> None:
        for cipher in self.ciphers:
            if cipher.uuid == uuid:
                return cipher
    
    def _find_zero(self) -> Cipher:
        for c in self.ciphers:
            if c.value == 0:
                return c
    
    def _find_dest(self, c: Cipher, origin_value: int, direction: str) -> Cipher:
        queue = deque([c])
        search_level = 0
        while queue:
            node = queue.popleft()
            search_level += 1
            if search_level == abs(origin_value):
                # print(f"{origin_value} will be inserted to the {direction} of {node}")
                return node
            else:
                queue.append(getattr(node, direction))


    def move(self, c: Cipher) -> None:
        if c.value == 0:
            return

        l = c.left
        r = c.right
        self.unlink(c)

        if c.value > 0:
            dest = self._find_dest(r, c.value, "right")
            self.insert(c, dest, dest.right)
        elif c.value < 0:
            dest = self._find_dest(l, c.value, "left")
            self.insert(c, dest.left, dest)
    
    def get_state(self):
        current = self.ciphers[0]
        visited = []
        while current.right not in visited:
            visited.append(current)
            current = current.right
        return [c.value for c in visited]
    
    def print_state(self):
        print(self.get_state())
    
    def run(self):
        for idx in range(len(self.ciphers)):
            cur_uuid = self.pointers[idx%len(self.pointers)]
            self.move(self._find_cipher(cur_uuid))
        self.print_state()
    
    def solve(self, *nth_values: int) -> int:
        total = 0

        max_nth = max(nth_values)
        step = 0
        current = self._find_zero()
        while step <= max_nth:
            current = current.right
            step += 1
            if step in nth_values:
                print(f"{step}th: {current}")
                total += current.value
        
        return total


ciphers = []
with open("test.txt") as f:
# with open("input.txt") as f:
    for line in f.readlines():
        c = Cipher(int(line.strip()))
        if len(ciphers) > 0:
            Encrypted.link(ciphers[-1], c)
        ciphers.append(c)

Encrypted.link(ciphers[-1], ciphers[0])


e = Encrypted(ciphers)
e.run()
answer_1 = e.solve(*[1000, 2000, 3000])
print(answer_1)
