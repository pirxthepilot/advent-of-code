from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


@dataclass
class Tile:
    gear: str = "."
    beams: Set[str] = field(default_factory=set)

    def add_beam(self, dir: str) -> None:
        self.beams.add(dir)


class Contraption:
    def __init__(self, tiles: Dict[Tuple[int, int], Tile], cols: int, rows: int):
        self.tiles = tiles
        self.cols = cols
        self.rows = rows

    def _is_outside(self, xyd: Tuple[int, int, str]) -> bool:
        x, y, _ = xyd
        return (
            x < 0 or
            x >= self.cols or
            y < 0 or
            y >= self.rows
        )

    def draw(self) -> None:
        display = ""
        for (x, y), tile in self.tiles.items():
            display += str(len(tile.beams)) if tile.beams else tile.gear
            if x != 0 and x % (self.cols - 1) == 0:
                display += "\n"
        print(display)

    def traverse(self) -> None:
        queue = deque([(0, 0, ">")])

        while queue:
            x, y, dir = queue.popleft()
            tile = self.tiles[(x, y)]
            if dir in tile.beams:
                continue
            tile.add_beam(dir)

            next = None
            if tile.gear == "\\":
                if dir == ">":
                    next = (x, y+1, "v")
                elif dir == "<":
                    next = (x, y-1, "^")
                elif dir == "^":
                    next = (x-1, y, "<")
                elif dir == "v":
                    next = (x+1, y, ">")
                if not self._is_outside(next):
                    queue.append(next)
            elif tile.gear == "/":
                if dir == ">":
                    next = (x, y-1, "^")
                elif dir == "<":
                    next = (x, y+1, "v")
                elif dir == "^":
                    next = (x+1, y, ">")
                elif dir == "v":
                    next = (x-1, y, "<")
                if not self._is_outside(next):
                    queue.append(next)
            elif tile.gear == "|" and dir in (">", "<"):
                for next in ((x, y-1, "^"), (x, y+1, "v")):
                    if not self._is_outside(next):
                        queue.append(next)
            elif tile.gear == "-" and dir in ("^", "v"):
                for next in ((x-1, y, "<"), (x+1, y, ">")):
                    if not self._is_outside(next):
                        queue.append(next)
            else:
                if dir == ">":
                    next = (x+1, y, ">")
                elif dir == "<":
                    next = (x-1, y, "<")
                elif dir == "^":
                    next = (x, y-1, "^")
                elif dir == "v":
                    next = (x, y+1, "v")
                if not self._is_outside(next):
                    queue.append(next)

    @property
    def energized(self) -> int:
        return sum([1 for t in self.tiles.values() if t.beams])


def s1(cont: Contraption) -> int:
    cont.traverse()
    # cont.draw()
    return cont.energized


tiles = {}
with open(FILE, "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, gear in enumerate(line.strip()):
            tiles[(x, y)] = Tile(gear)

cont = Contraption(tiles, x + 1, y + 1)
print(s1(cont))
