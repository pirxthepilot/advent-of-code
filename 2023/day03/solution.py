"""
Data structure

{
    (x, y): value,
    ...
}
"""
from collections import defaultdict
from typing import Dict, List, Set


with open("input.txt", "r") as f:
    text = [t.strip() for t in f.readlines()]


class Engine:
    def __init__(self, text: str):
        self.engine = {}
        self.numbers = []

        for y, line in enumerate(text):
            current_num_idxs = []
            for x, c in enumerate(line):
                idx = (x, y)
                if c != ".":
                    self.engine[idx] = c

                if c.isnumeric():
                    current_num_idxs.append(idx)
                    if x == len(line) - 1:  # EOL
                        self.numbers.append(current_num_idxs)
                        current_num_idxs = []
                elif current_num_idxs:
                    self.numbers.append(current_num_idxs)
                    current_num_idxs = []

    def _idxs_to_num(self, idxs: list) -> int:
        return int("".join([self.engine[i] for i in idxs]))
    
    def _get_adjacents(self, x: int, y: int) -> List[tuple]:
        return [
            (x,   y-1),  # N
            (x+1, y-1),  # NE
            (x+1, y),    # E
            (x+1, y+1),  # SE
            (x,   y+1),  # S
            (x-1, y+1),  # SW
            (x-1, y),    # W
            (x-1, y-1),  # NW
        ]
    
    @property
    def valid_part_numbers(self) -> List[int]:
        valid = []
        for idxs in self.numbers:
            current_num = self._idxs_to_num(idxs)
            # Look for adjacent symbols
            is_valid = False
            for idx in idxs:
                x, y = idx
                for a_idx in self._get_adjacents(x, y):
                    adjacent_c = self.engine.get(a_idx)
                    if adjacent_c and not adjacent_c.isnumeric():
                        valid.append(current_num)
                        is_valid = True
                        break
                if is_valid:
                    break
        return valid

    @property
    def total_parts(self) -> int:
        return sum(self.valid_part_numbers)
    
    @property
    def gears(self) -> Dict[tuple, Set[int]]:
        potential_gears = defaultdict(set)
        for idxs in self.numbers:
            current_num = self._idxs_to_num(idxs)
            # Look for neighboring gears
            for idx in idxs:
                x, y = idx
                for a_idx in self._get_adjacents(x, y):
                    adjacent_c = self.engine.get(a_idx)
                    if adjacent_c == "*":
                        potential_gears[a_idx].add(current_num)
        return {gear_idx: parts for gear_idx, parts in potential_gears.items() if len(parts) == 2}

    @property
    def gear_ratios_total(self) -> int:
        ratios = []
        for parts in self.gears.values():
            g1, g2 = parts
            ratios.append(g1 * g2)
        return sum(ratios)


def s1(engine: Engine) -> int:
    return engine.total_parts

def s2(engine: Engine) -> int:
    return engine.gear_ratios_total


engine = Engine(text)
print(s1(engine))
print(s2(engine))
