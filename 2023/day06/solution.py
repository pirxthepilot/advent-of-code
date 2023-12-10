import math
import sys
from dataclasses import dataclass
from typing import List, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


@dataclass
class Race:
    time: int
    record: int

    def compute_potential_range(self) -> Tuple[int]:
        # Wow, quadratic equations
        a = 1
        b = -self.time
        c = self.record + 1
        x1 = (-b+math.sqrt((b**2)-(4*(a*c))))/(2*a)
        x2 = (-b-math.sqrt((b**2)-(4*(a*c))))/(2*a)
        return (
            math.floor(x1),
            math.ceil(x1),
            math.floor(x2),
            math.ceil(x2),
        )

    def compute_distance(self, hold_ms: int) -> int:
        return (self.time - hold_ms) * hold_ms

    @property
    def win_count(self) -> int:
        wins = 0

        for hold_ms in range(self.time - 1, 0, -1):
            distance_mm = self.compute_distance(hold_ms)
            if distance_mm > self.record:
                wins += 1
            elif wins:
                break
        return wins
    
    @property
    def win_count_with_math(self) -> int:
        winning_hold_range = []
        for hold_ms in self.compute_potential_range():
            distance_mm = self.compute_distance(hold_ms)
            # print(f"Hold for {hold_ms}ms = {distance_mm}mm")
            if distance_mm > self.record:
                winning_hold_range.append(hold_ms)
        return max(winning_hold_range) - min(winning_hold_range) + 1


class Races:
    def __init__(self, text: str):
        self.races = []

        times = self._line_to_nums(text[0])
        recs = self._line_to_nums(text[1])

        for idx in range(len(times)):
            self.races.append(Race(times[idx], recs[idx]))
    
    def __iter__(self):
        return iter(self.races)

    @staticmethod
    def _line_to_nums(line: str) -> List[int]:
        return [int(i.strip())
                for i in line.split(":")[1].strip().split(" ")
                if i]
    
    def margin_of_error(self) -> int:
        wins = 1
        for w in [r.win_count_with_math for r in self]:
            wins *= w
        return wins


def s1() -> int:
    races = Races(text)
    return races.margin_of_error()

def s2() -> int:
    races = Races([l.replace(" ", "") for l in text])
    return races.margin_of_error()


print(s1())
print(s2())
