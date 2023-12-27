from __future__ import annotations

import sys
from collections import deque
from typing import Dict, List, Optional, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


# Similar to Day 10 class
class Rock:
    def __init__(self, x: int, y: int, type_: str = "O"):
        self.x = x
        self.y = y
        self.type_ = type_
        self.n: Optional[Rock] = None
        self.e: Optional[Rock] = None
        self.s: Optional[Rock] = None
        self.w: Optional[Rock] = None

    def __repr__(self) -> str:
        return self.type_
    
    @staticmethod
    def _opposite(direction: str) -> str:
        if direction == "n":
            return "s"
        if direction == "s":
            return "n"
        if direction == "e":
            return "w"
        if direction == "w":
            return "e"
    
    def set_neighbor(self, direction: str, other: Rock) -> None:
        # Connect self and other
        setattr(self, direction, other)
        if getattr(other, direction) is not None:
            other.set_neighbor(self._opposite(direction), self)


class Platform:
    def __init__(self):
        self.rocks: Dict[Tuple[int, int], Rock] = {}
        self.row_count: int = 0
        self.col_count: int = 0
        self._queue_order: Dict[str, List[Tuple[int, int]]] = {}

    def __getitem__(self, coord: Tuple[int, int]) -> Rock:
        return self.rocks[coord]

    def _get_queue_order(self, direction: str) -> List[Tuple[int, int]]:
        if direction in self._queue_order:
            return self._queue_order[direction]
        
        order = []
        if direction == "n":
            for y in range(self.row_count):
                for x in range(self.col_count):
                    order.append((x, y))
        return order

    def draw(self) -> str:
        display = ""
        for x, y in self._get_queue_order("n"):
            display += self[(x, y)].type_ if (x, y) in self.rocks else "."
            if x != 0 and x % (self.col_count - 1) == 0:
                display += "\n"
        return display
    
    def add_rock(self, x, y, type_: str = "O") -> None:
        if (x, y) in self.rocks:
            raise Exception(f"Rock ({x}, {y}) already exists")

        # Instantiate and add rock to our collection
        rock = Rock(x, y, type_)
        self.rocks[(x, y)] = rock

        # Find northern neighbor
        for iy in range(y - 1, -1, -1):
            if (x, iy) in self.rocks:
                rock.set_neighbor("n", self[(x, iy)])
                return
    
    def move_rock(self, rock: Rock, new_x: int, new_y: int) -> None:
        if rock.x == new_x and rock.y == new_y:
            return
        old_x = rock.x
        old_y = rock.y
        rock.x = new_x
        rock.y = new_y
        self.rocks[(new_x, new_y)] = rock
        del self.rocks[(old_x, old_y)]
    
    def tilt(self, direction: str) -> None:
        if direction == "n":
            visited = set()
            for x, y in self._get_queue_order(direction):
                if (
                    (x, y) in visited or
                    (x, y) not in self.rocks
                ):
                    continue
                visited.add((x, y))
                rock = self[(x, y)]
                if rock.type_ == "O":
                    if rock.n is None:
                        self.move_rock(rock, x, 0)
                    else:
                        self.move_rock(rock, x, rock.n.y + 1)

    def _gen_load_map(self) -> Dict[int, int]:
        return {y: self.row_count - y for y in range(self.row_count)}

    @property
    def total_load(self) -> int:
        total = 0
        load_map = self._gen_load_map()
        for x, y in self._get_queue_order("n"):
            if (x, y) in self.rocks and  self[(x, y)].type_ == "O":
                total += load_map[y]
        return total


def s1(platform: Platform) -> int:
    # print("Before:")
    # print(platform.draw())
    platform.tilt("n")
    # print("After:")
    # print(platform.draw())
    return platform.total_load


platform = Platform()
with open(FILE, "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line):
            if c in ("O", "#"):
                platform.add_rock(int(x), int(y), c)
    platform.row_count = y + 1
    platform.col_count = x


print(s1(platform))
