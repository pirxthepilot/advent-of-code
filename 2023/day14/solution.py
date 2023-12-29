from __future__ import annotations

import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


def opposite(direction: str) -> str:
    if direction == "n":
        return "s"
    if direction == "s":
        return "n"
    if direction == "e":
        return "w"
    if direction == "w":
        return "e"
    

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
    
    def set_neighbor(self, direction: str, other: Optional[Rock]) -> None:
        setattr(self, direction, other)
        if (
            other is not None and
            getattr(other, opposite(direction)) != self
        ):
            other.set_neighbor(opposite(direction), self)


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

    def _find_neighbor(self, rock: Rock, direction: str) -> None:
        search_order = {
            "n": (None, range(rock.y - 1, -1, -1)),
            "s": (None, range(rock.y + 1, self.row_count)),
            "e": (range(rock.x + 1, self.col_count), None),
            "w": (range(rock.x -1, -1, -1), None),
        }
        x_ord, y_ord = search_order[direction]
        locs = x_ord if y_ord is None else y_ord
        for i in locs:
            other: Tuple[int, int] = (
                i if x_ord else rock.x,
                i if y_ord else rock.y
            )
            if (
                other in self.rocks and
                getattr(self[other], opposite(direction)) is not self
            ):
                rock.set_neighbor(direction, self[other])
                break
            else:
                rock.set_neighbor(direction, None)

    def _update_all(self) -> None:
        """ Update all rocks' neighbors """
        for rock in self.rocks.values():
            self._find_neighbor(rock, "n")
            self._find_neighbor(rock, "s")
            self._find_neighbor(rock, "e")
            self._find_neighbor(rock, "w")

    def add_rock(self, x, y, type_: str = "O") -> None:
        if (x, y) in self.rocks:
            raise Exception(f"Rock ({x}, {y}) already exists")

        # Instantiate and add rock to our collection
        rock = Rock(x, y, type_)
        self.rocks[(x, y)] = rock
        self._find_neighbor(rock, "n")
        self._find_neighbor(rock, "w")

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
        # Go through each rock and update neighbors
        self._update_all()

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

    def cycle(self, count: int = 1) -> None:
        for count in range(count):
            for d in ("n", "w", "s", "e"):
                self.tilt(d)


def s1(platform: Platform) -> int:
    platform.tilt("n")
    return platform.total_load


def s2(platform: Platform) -> int:
    print("Before:")
    platform.draw()
    # platform.cycle(1000000000)
    platform.cycle(3)
    print("Cycle:")
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


print(s1(platform))
print(s2(platform))
