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
    def _get_mirror_line(values: List[str]) -> Optional[int]:
    # def _get_mirror_line(values: List[str]) -> Shape:
        l_val = ""
        for r_idx, r_val in enumerate(values):
            # Find instances where two values are identical
            if r_val != l_val:
                l_val = r_val
                continue
            
            # Get l_idx from position of r_idx
            l_idx = r_idx - 1

            # Fan outward both ways from the identical values to
            # determine mirror effect
            distance = 0
            while l_idx - distance >= 0 and r_idx + distance < len(values):
                # print(l_idx, r_idx, distance, len(values))
                if values[l_idx - distance] == values[r_idx + distance]:
                    distance += 1
                else:
                    break
            
            # If at the points in the distance are in either edge, it means that
            # the line is between l_idx and r_idx
            if (
                distance != 0 and  # Assume line does not occur near edges
                (l_idx - distance + 1 == 0 or r_idx + distance == len(values))
            ):
                return l_idx + 1
        return None
    
    def get_vertical_line(self) -> Optional[int]:
        return self._get_mirror_line(self.cols)

    def get_horizontal_line(self) -> int:
        return self._get_mirror_line(self.rows)


@dataclass
class Maps:
    maps: List[Map]

    def __iter__(self) -> Iterable[Map]:
        return iter(self.maps)

    def summarize(self) -> int:
        sum_vertical = 0
        sum_horizontal = 0
        for m in maps:
            # print(f"\nEval:\n{m}\n")
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


maps = Maps(get_maps())
print(s1(maps))
