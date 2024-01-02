import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Set, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


def opposite(dir: str) -> str:
    if dir == "^":
        return "v"
    if dir == "v":
        return "^"
    if dir == ">":
        return "<"
    if dir == "<":
        return ">"


@dataclass
class Route:
    path: List[Tuple[int, int]]
    dir: str = ">"
    straight: int = 1
    loss: int = 0

    def __repr__(self) -> str:
        return f"{len(self.path)} blocks in route with heat loss of {self.loss}"


class Map:
    def __init__(self, blocks: Dict[Tuple[int, int], int], cols: int, rows: int):
        self.blocks = blocks
        self.cols = cols
        self.rows = rows

    def draw(self) -> None:
        display = ""
        for (x, _), loss in self.blocks.items():
            display += str(loss)
            if x != 0 and x % (self.cols - 1) == 0:
                display += "\n"
        print(display)

    def _is_outside(self, xy: Tuple[int, int]) -> bool:
        x, y = xy
        return (
            x < 0 or
            x >= self.cols or
            y < 0 or
            y >= self.rows
        )

    def _routes(self, start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Route]:
        queue = deque([Route([start], "", 0, 0)])
        cache: Dict[Tuple[int, int, int, str], int] = {}

        while queue:
            route = queue.popleft()
            vertex = route.path[-1]

            x, y = vertex
            cache_key = (x, y, route.straight, route.dir)
            if (
                cache.get(cache_key) and
                cache[cache_key] < route.loss
            ):
                continue

            if vertex == end:
                yield route

            # print(f"Eval: {len(route.path)} blocks with {route.loss} loss")

            cache[cache_key] = route.loss
            ignore_dirs = set([opposite(route.dir)])
            if route.straight == 3:
                ignore_dirs.add(route.dir)

            for next_dir, next_xy in {
                "^": (x, y-1),  # n
                ">": (x+1, y),  # e
                "v": (x, y+1),  # s
                "<": (x-1, y),  # w
            }.items():
                if (
                    next_dir not in ignore_dirs and
                    next_xy not in route.path and
                    not self._is_outside(next_xy)
                ):
                    if route.straight == 3 or route.dir != next_dir:
                        new_straight = 1
                    else:
                        new_straight = route.straight + 1

                    next_route = Route(
                        route.path + [next_xy],
                        next_dir,
                        new_straight,
                        route.loss + self.blocks[next_xy],
                    )

                    queue.append(next_route)

    def best_route(self) -> int:
        best = None
        for route in self._routes((0, 0), (self.cols-1, self.rows-1)):
            if (
                best is None or
                route.loss < best
            ):
                best = route.loss
                print(f"==== [BEST] {route.loss} traversing {len(route.path)} blocks")
        return best


def s1(m: Map) -> int:
    return m.best_route()


blocks = {}
with open(FILE, "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, loss in enumerate(line.strip()):
            blocks[(x, y)] = int(loss)

m = Map(blocks, x+1, y+1)
print(s1(m))
