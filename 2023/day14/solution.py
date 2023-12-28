from __future__ import annotations

import sys
from collections import defaultdict
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
        # return self.type_
        return f"({self.x},{self.y}):{self.type_}"
    
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
        setattr(self, direction, other)
        if getattr(other, self._opposite(direction)) != self:
            other.set_neighbor(self._opposite(direction), self)


class Platform:
    def __init__(self):
        self.rocks: Dict[Tuple[int, int], Rock] = {}
        self.row_count: int = 0
        self.col_count: int = 0
        self._queue_order: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self._load_map: Dict[int, int] = {}

    def __getitem__(self, coord: Tuple[int, int]) -> Rock:
        return self.rocks[coord]

    def _get_queue_order(self, direction: str) -> List[Tuple[int, int]]:
        if direction not in self._queue_order:
            if direction == "n":
                for y in range(self.row_count):
                    for x in range(self.col_count):
                        self._queue_order[direction].append((x, y))
            elif direction == "e":
                for x in range(self.col_count - 1, -1, -1):
                    for y in range(self.row_count - 1, -1, -1):
                        self._queue_order[direction].append((x, y))
            elif direction == "s":
                for y in range(self.row_count - 1, -1, -1):
                    for x in range(self.col_count - 1, -1, -1):
                        self._queue_order[direction].append((x, y))
            elif direction == "w":
                for x in range(self.col_count):
                    for y in range(self.row_count):
                        self._queue_order[direction].append((x, y))

        return self._queue_order[direction]

    def draw(self) -> None:
        display = ""
        for x, y in self._get_queue_order("n"):
            display += self[(x, y)].type_ if (x, y) in self.rocks else "."
            if x != 0 and x % (self.col_count - 1) == 0:
                display += "\n"
        print(display)

    def _update_neighbors(self, rock: Rock, direction: str = "n") -> None:
        # Search order
        y_search_order: List[int] = []
        x_search_order: List[int] = []

        if direction in ("n", "w"):
            y_search_order = list(range(rock.y - 1, -1, -1))
            x_search_order = list(range(rock.x - 1, -1, -1))
        elif direction in ("s", "e"):
            y_search_order = list(range(rock.y, self.row_count - 1))
            x_search_order = list(range(rock.x, self.col_count - 1))

        # Link with n/s neighbor
        # for iy in range(rock.y - 1, -1, -1):
        for iy in y_search_order:
            if (x, iy) in self.rocks:
                rock.set_neighbor(
                    "n" if direction in ("n", "w") else "s",
                    self[(x, iy)]
                )
                # print(f"{rock} n neighbor is {rock.n}")
                # print(f"  inverse: {rock.n.s}")
                break

        # Link with e/w neighbor
        for ix in x_search_order:
            if (ix, y) in self.rocks:
                rock.set_neighbor(
                    "w" if direction in ("n", "w") else "e",
                    self[(ix, y)]
                )
                # print(f"{rock} w neighbor is {rock.w}")
                # print(f"  inverse: {rock.w.e}")
                break

    def add_rock(self, x, y, type_: str = "O") -> None:
        if (x, y) in self.rocks:
            raise Exception(f"Rock ({x}, {y}) already exists")

        # Instantiate and add rock to our collection
        rock = Rock(x, y, type_)
        self.rocks[(x, y)] = rock
        self._update_neighbors(rock)

    def move_rock(self, rock: Rock, new_x: int, new_y: int) -> None:
        if rock.x == new_x and rock.y == new_y:
            return
        old_x = rock.x
        old_y = rock.y
        rock.x = new_x
        rock.y = new_y
        self.rocks[(new_x, new_y)] = rock
        del self.rocks[(old_x, old_y)]

    def _update_all_rocks(self) -> None:
        for x, y in self._get_queue_order("n"):
            if (x, y) in self.rocks:
                self._update_neighbors(self[(x, y)])

    def tilt(self, direction: str) -> None:
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
                if direction == "n":
                    if rock.n is None:
                        self.move_rock(rock, x, 0)
                    else:
                        self.move_rock(rock, x, rock.n.y + 1)
                elif direction == "e":
                    if rock.e is None:
                        self.move_rock(rock, self.col_count - 1, y)
                    else:
                        self.move_rock(rock, rock.e.x - 1, y)
                elif direction == "s":
                    if rock.s is None:
                        self.move_rock(rock, x, self.row_count - 1)
                    else:
                        self.move_rock(rock, x, rock.s.y - 1)
                elif direction == "w":
                    if rock.w is None:
                        self.move_rock(rock, 0, y)
                    else:
                        self.move_rock(rock, rock.w.x + 1, y)
                # self._update_neighbors(rock, direction)
        # Go through each rock and update neighbors
        self._update_all_rocks()

    def _get_load_map(self) -> Dict[int, int]:
        if not self._load_map:
            self._load_map = {y: self.row_count - y for y in range(self.row_count)}
        return self._load_map

    @property
    def total_load(self) -> int:
        total = 0
        for x, y in self._get_queue_order("n"):
            if (x, y) in self.rocks and  self[(x, y)].type_ == "O":
                total += self._get_load_map()[y]
        return total


def s1(platform: Platform) -> int:
    platform.tilt("n")
    return platform.total_load


def s2(platform: Platform) -> int:
    print("Before:")
    platform.draw()
    # for d in ("n", "w", "s", "e"):
    for d in ("e", "s"):
        print(f"Tilt {d}:")
        platform.tilt(d)
        platform.draw()
    return platform.total_load


platform = Platform()
with open(FILE, "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line):
            if c in ("O", "#"):
                platform.add_rock(int(x), int(y), c)
    platform.row_count = y + 1
    platform.col_count = x


# print(s1(platform))
print(s2(platform))
