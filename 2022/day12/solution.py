from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


CWD = Path(__file__).resolve().parent


@dataclass
class Location:
    x: int
    y: int
    height: str
    start: bool = False
    end: bool = False
    traversable: List[Location] = field(default_factory=lambda: [])

    def __hash__(self):
        return hash((self.x, self.y, self.height))


class Map:
    def __init__(self, heightmap):
        self.hmap = heightmap
        self.start, self.end = self._process_map()

    @staticmethod
    def _is_traversable(here: Location, neighbor: Location) -> bool:
        return ord(neighbor.height) - ord(here.height) <= 1

    def _get_traversable_neighbors(self, loc: Location) -> None:
        # print(f"Getting neighbors: {loc}")
        possible_neighbors = []
        if loc.y - 1 >= 0:
            possible_neighbors.append(self.hmap[loc.y-1][loc.x])  # North
        if loc.x + 1 < len(self.hmap[0]):
            possible_neighbors.append(self.hmap[loc.y][loc.x+1])  # East
        if loc.y + 1 < len(self.hmap):
            possible_neighbors.append(self.hmap[loc.y+1][loc.x])  # South
        if loc.x - 1 >= 0:
            possible_neighbors.append(self.hmap[loc.y][loc.x-1])  # West

        for neighbor in possible_neighbors:
            if self._is_traversable(loc, neighbor):
                # print("  TRAVERSABLE!")
                loc.traversable.append(neighbor)

    def _process_map(self):
        start = None
        for row in self.hmap:
            for loc in row:
                # Start and end
                if loc.start:
                    start = loc
                elif loc.end:
                    end = loc

                # Find traversable neighbors
                self._get_traversable_neighbors(loc)
        return (start, end)

    def print_map(self):
        for row in self.hmap:
            print([i.height for i in row])

    def print_info(self, x: int, y: int) -> List[Location]:
        loc = self.hmap[y][x]
        print(f"Location ({loc.x}, {loc.y})")
        print(f"  Height: {loc.height}")
        print("  Traversable:")
        for t in loc.traversable:
            print(f"    Location ({t.x}, {t.y}) height={t.height}")

    def find_shortest_path(self, start: Location, end: Location) -> list:
        # BFS again to the rescue
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            vertex = path[-1]
            if vertex == end:
                return path
            elif vertex not in visited:
                for neighbor in vertex.traversable:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    visited.add(vertex)

    def find_path_with_best_starting_point(self) -> list:
        shortest_path = None
        for row in self.hmap:
            for loc in row:
                if loc.height == "a":
                    print(f"Finding path starting with ({loc.x}, {loc.y}) with height {loc.height}...")
                    path = self.find_shortest_path(loc, self.end)
                    if not path:
                        print("  No route found :(")
                        continue
                    print(f"  Found {len(path)} locations ({len(path) - 1} steps)!")
                    if shortest_path is None:
                        shortest_path = path
                    elif len(path) < len(shortest_path):
                        print("  This is the shortest so far!")
                        shortest_path = path
        return shortest_path


heightmap = []
# with open(CWD / "test.txt") as f:
with open("input.txt") as f:
    for y, line in enumerate(f.readlines()):
        row = []
        for x, value in enumerate(line.strip()):
            if value == "S":
                row.append(Location(x, y, "a", start=True))
            elif value == "E":
                row.append(Location(x, y, "z", end=True))
            else:
                row.append(Location(x, y, value))
        heightmap.append(row)


m = Map(heightmap)
# m.print_map()


# Part 1

# m.print_info(m.start.x, m.start.y)
# m.print_info(m.end.x, m.end.y)
# print([(i.x, i.y) for i in m.find_shortest_path(m.start, m.end)])
answer_1 = len(m.find_shortest_path(m.start, m.end)) - 1
print(answer_1)


# Part 2

answer_2 = len(m.find_path_with_best_starting_point()) - 1
print(answer_2)
