import sys
from typing import List


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Sequence:
    def __init__(self, *steps: str):
        self.steps = steps
    
    @staticmethod
    def _compute_hash(step: str) -> int:
        hash = 0
        for c in step:
            hash += ord(c)
            hash = (hash * 17) % 256
        return hash
    
    def sum_of_results(self) -> int:
        return sum([self._compute_hash(s) for s in self.steps])


def s1(seq: Sequence) -> int:
    return seq.sum_of_results()


seq = Sequence(*text[0].split(","))
print(s1(seq))
