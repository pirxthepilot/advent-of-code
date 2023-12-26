from __future__ import annotations

import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from time import sleep
from typing import Iterable, List, Optional, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


def render(text: str) -> None:
    sleep(0.18)
    os.system("clear")
    print(text)


class Map:
    def __init__(self, rows: List[str], cols: List[str]):
        self.rows = rows
        self.cols = cols
    
    def __repr__(self) -> str:
        return "\n".join(self.rows)

    @staticmethod
    def _get_mirror_line(values: List[str], ignore: Optional[int] = None) -> Optional[int]:
        l_val = ""
        for r_idx, r_val in enumerate(values):
            # Find instances where two values are identical
            if r_val != l_val:
                l_val = r_val
                continue

            # Ignore result (if specified)
            if r_idx == ignore:
                continue

            # Get l_idx from position of r_idx
            l_idx = r_idx - 1

            # Fan outward both ways from the identical values to
            # determine mirror effect
            distance = 0
            while l_idx - distance >= 0 and r_idx + distance < len(values):
                if values[l_idx - distance] == values[r_idx + distance]:
                    distance += 1
                else:
                    break
            
            # If at the points in the distance are in either edge, it means that
            # the line is between l_idx and r_idx
            if (
                # distance != 0 and  # Assume line does not occur near edges
                (l_idx - distance + 1 == 0 or r_idx + distance == len(values))
            ):
                return r_idx
        return None
    
    def get_vertical_line(self, ignore: Optional[int] = None) -> Optional[int]:
        return self._get_mirror_line(self.cols, ignore)

    def get_horizontal_line(self, ignore: Optional[int] = None) -> Optional[int]:
        return self._get_mirror_line(self.rows, ignore)


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

    @staticmethod
    def _find_smudged(m: Map) -> Tuple[Optional[int]]:
        og_v = m.get_vertical_line()
        og_h = m.get_horizontal_line()

        for y in range(len(m.rows)):
            for x in range(len(m.cols)):
                new_val = "#" if m.rows[y][x] == "." else "."
                new_row = f"{m.rows[y][:x]}{new_val}{m.rows[y][x+1:]}"
                new_col = f"{m.cols[x][:y]}{new_val}{m.cols[x][y+1:]}"
                new_m = Map(
                    m.rows[:y] + [new_row] + m.rows[y+1:],
                    m.cols[:x] + [new_col] + m.cols[x+1:]
                )
                new_v = new_m.get_vertical_line(ignore=og_v)
                new_h = new_m.get_horizontal_line(ignore=og_h)
                # render(f"\nVar:\n{new_m}\n({new_v}, {new_h})")
                if (
                    (og_v and new_v and og_v != new_v) or
                    (og_h and new_v)
                ):
                    return new_v, None
                if (
                    (og_h and new_h and og_h != new_h) or
                    (og_v and new_h)
                ):
                    return None, new_h
        raise Exception("No smudge found wonk wonk")

    def desmudged(self) -> int:
        sum_v = 0
        sum_h = 0
        for m in maps:
            # print(f"\nEval:\n{m}")
            new_v, new_h = self._find_smudged(m)
            if new_v:
                sum_v += new_v
            else:
                sum_h += new_h
        return sum_v + (100 * sum_h)


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

def s2(maps: Maps) -> int:
    return maps.desmudged()


maps = Maps(get_maps())
print(s1(maps))
print(s2(maps))
