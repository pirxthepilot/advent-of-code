from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List, Optional


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


@dataclass
class Value:
    value: int
    lp: Optional[Value] = None
    rp: Optional[Value] = None
    l: Optional[Value] = None
    r: Optional[Value] = None

    def __repr__(self) -> str:
        return str(self.value)

    def __add__(self, other: Value) -> int:
        return self.value + other.value

    def __sub__(self, other: Value) -> int:
        return self.value - other.value


class History:
    def __init__(self, history: List[int]):
        self.values = history

    @staticmethod
    def _all_values_zero(values: List[int]) -> bool:
        for v in values:
            if v != 0:
                return False
        return True

    def next_value(self) -> int:
        # Get the intervals
        current_values = self.values
        levels = [current_values]
        while not self._all_values_zero(current_values):
            new_values = []
            last_v = None
            for v in current_values:
                if last_v is not None:
                    new_values.append(v - last_v)
                last_v = v
            current_values = new_values
            levels.append(current_values)
        
        # Walk back to get next value
        ends = [v[-1] for v in levels]
        ends.reverse()

        next_values = []
        for idx, value in enumerate(ends):
            if idx == 0:
                continue
            if not next_values:
                next_values.append(value + ends[idx-1])
            else:
                next_values.append(next_values[-1] + ends[idx])

        return next_values[-1]


def s1(text: str) -> int:
    sum = 0
    for line in text:
        history = History([int(i) for i in line.split(" ")])
        sum += history.next_value()
    return sum


print(s1(text))
