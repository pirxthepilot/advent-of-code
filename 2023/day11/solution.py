import sys
from collections import deque
from itertools import combinations
from typing import List, Iterable, Set, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Image:
    expansion_shift = 1

    def __init__(self, text: str):
        # Original
        galaxies = []
        all_x = set()
        all_y = set()
        for y, line in enumerate(text):
            all_y.add(y)    
            for x, point in enumerate(line):
                all_x.add(x)
                if point == "#":
                    galaxies.append((x, y))
        
        # Expanded
        self.galaxies, self.max_x, self.max_y = self._expanded(galaxies, all_x, all_y)

        self.pairs = list(combinations(self.galaxies, 2))

    def _expanded(
        self,
        galaxies: List[Tuple[int]],
        all_x: Set[int],
        all_y: Set[int]
    ) -> Tuple[List[Tuple[int]], int, int]:
        filled_cols = set()
        filled_rows = set()

        for x, y in galaxies:
           filled_cols.add(x)
           filled_rows.add(y) 
        
        empty_cols = set(all_x) - filled_cols
        empty_rows = set(all_y) - filled_rows

        new_galaxies = []
        for x, y in galaxies:
            # Shift right (x)
            x_shifts = 0
            for e_x in empty_cols:
                if x > e_x:
                    x_shifts += self.expansion_shift

            # Shift down (y)
            y_shifts = 0
            for e_y in empty_rows:
                if y > e_y:
                    y_shifts += self.expansion_shift

            new_galaxies.append((x + x_shifts, y + y_shifts))

        return (new_galaxies,
                max(all_x) + len(empty_cols),
                max(all_y) + len(empty_rows))


    def _get_neighbors(self, x: int, y: int) -> Iterable[Tuple[int]]:
        for n in (
            (x,   y-1),  # N
            (x+1, y),    # E
            (x,   y+1),  # S
            (x-1, y),    # W
        ):
            if x <= self.max_x and y <= self.max_y:
                yield n

    def _find_shortest_distance(self, start: Tuple[int], end: Tuple[int]) -> int:
        sx, sy = start
        ex, ey = end
        return abs(ex - sx) + abs(ey - sy)
    
    def distance_sum(self) -> int:
        sum = 0
        for start, end in self.pairs:
            sum += self._find_shortest_distance(start, end)
        return sum


class Image1M(Image):
    expansion_shift = 1000000 - 1


def s1(text: str) -> int:
    image = Image(text)
    return image.distance_sum()

def s2(text: str) -> int:
    image = Image1M(text)
    return image.distance_sum()


print(s1(text))
print(s2(text))
