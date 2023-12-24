from __future__ import annotations

import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Iterable, List, Optional


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


@dataclass
class Shape:
    l: int
    r: int
    l_side: list = field(default_factory=list)
    r_side: list = field(default_factory=list)

    def __eq__(self, other: Shape) -> bool:
        return (
            self.l == other.l and
            self.r == other.r
        )


class Map:
    def __init__(self, rows: List[str], cols: List[str]):
        self.rows = rows
        self.cols = cols
    
    def __repr__(self) -> str:
        return "\n".join(self.rows)

    @staticmethod
    def _get_mirror_line(values: List[str]) -> Shape:
        queue = deque([Shape(0, len(values)-1)])
        visited = []

        while queue:
            shape = queue.popleft()
            # if shape.l >= shape.r and shape.l_side:
            #     return shape
            if shape.l >= shape.r and shape.l_side:
                min_distance_to_edge = min(shape.l, len(values[0]) - shape.l)
                return shape, min_distance_to_edge
            if shape not in visited:
                # print(f"Comparing {shape}")
                visited.append(shape)
                if values[shape.l] == values[shape.r]:
                    new_l_side = shape.l_side + [values[shape.l]]
                    new_r_side = shape.r_side + [values[shape.r]]
                    if new_l_side == new_r_side:
                        # print("  Match")
                        queue.append(Shape(
                            shape.l+1,
                            shape.r-1,
                            new_l_side,
                            new_r_side
                        ))
                else:
                    queue.append(Shape(shape.l, shape.r-1))
                    queue.append(Shape(shape.l+1, shape.r))
    
    def get_vertical_line(self) -> Optional[int]:
        shape, min_distance = self._get_mirror_line(self.cols)
        print(f"Vert: {shape}")
        return shape.l if len(shape.l_side) >= min_distance - 1 else None
        # shape = self._get_mirror_line(self.cols)
        # print(shape)
        # return shape.l if len(shape.l_side) > 1 else None

    def get_horizontal_line(self) -> int:
        shape, min_distance = self._get_mirror_line(self.rows)
        print(f"Hori: {shape}")
        return shape.l if len(shape.l_side) >= min_distance - 1 else None
        # shape = self._get_mirror_line(self.rows)
        # print(shape)
        # return shape.l if len(shape.l_side) > 1 else None


@dataclass
class Maps:
    maps: List[Map]

    def __iter__(self) -> Iterable[Map]:
        return iter(self.maps)

    def summarize(self) -> int:
        sum_vertical = 0
        sum_horizontal = 0
        for m in maps:
            print(f"\nEval:\n{m}\n")
            v = m.get_vertical_line()
            if v:
                sum_vertical += v
            else:
                sum_horizontal += m.get_horizontal_line()
        return sum_vertical + (100 * sum_horizontal)


def get_maps() -> List[Map]:
    maps = []
    with open(FILE, "r") as f:
        rows = [] 
        cols = defaultdict(str) 
        for line in f.readlines():
            if line == "\n":
                maps.append(Map(rows, list(cols.values())))
                rows = []
                cols = defaultdict(str)
                continue

            rows.append(line.strip())
            for idx, c in enumerate(rows[-1]):
                cols[idx] += c
        maps.append(Map(rows, list(cols.values())))
    return maps


def s1(maps: Maps) -> int:
     return maps.summarize()
     # return maps.maps[0].get_vertical_line()


maps = Maps(get_maps())
print(s1(maps))
