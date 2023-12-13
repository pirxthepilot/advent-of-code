from __future__ import annotations

import sys
from typing import List


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class History:
    def __init__(self, history: List[int]):
        self.values = history

    @staticmethod
    def _all_values_zero(values: List[int]) -> bool:
        for v in values:
            if v != 0:
                return False
        return True

    def _get_intervals_list(self) -> List[List[int]]:
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
        return levels

    def next_value(self) -> int:
        # Walk back to get next value
        ends = [v[-1] for v in self._get_intervals_list()]
        ends.reverse()

        next_values = []
        for idx, value in enumerate(ends):
            if idx == 0:
                continue
            if not next_values:
                next_values.append(value + ends[idx-1])
            else:
                next_values.append(next_values[-1] + value)

        return next_values[-1]

    def previous_value(self) -> int:
        # Walk back to get previous value
        starts = [v[0] for v in self._get_intervals_list()]
        starts.reverse()

        previous_values = []
        for idx, value in enumerate(starts):
            if idx == 0:
                continue
            if not previous_values:
                previous_values.append(value - starts[idx-1])
            else:
                previous_values.append(value - previous_values[-1])

        return previous_values[-1]


def get_histories(text: str) -> List[History]:
    histories = []
    for line in text:
        histories.append(History([int(i) for i in line.split(" ")]))
    return histories


def s1(histories: List[History]) -> int:
    return sum([h.next_value() for h in histories])


def s2(histories: List[History]) -> int:
    return sum([h.previous_value() for h in histories])


histories = get_histories(text)
print(s1(histories))
print(s2(histories))
