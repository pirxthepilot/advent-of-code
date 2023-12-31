from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


def compute_hash(text: str) -> int:
    hash = 0
    for c in text:
        hash += ord(c)
        hash = (hash * 17) % 256
    return hash


class Boxes:
    def __init__(self):
        # {
        #   hash: {
        #     label: focal_length,
        #     (..)
        #   },
        #   (..)
        # }
        self.boxes: Dict[int, Dict[str, str]] = defaultdict(dict)
    
    def process_step(self, step: str) -> None:
        steps = step.split("=")

        if len(steps) == 2:
            label, focal_length = steps
            self.boxes[compute_hash(label)][label] = int(focal_length)
        else:
            label = steps[0].split("-")[0]
            hash = compute_hash(label)
            if self.boxes[hash].get(label):
                del self.boxes[hash][label]

    def power(self) -> int:
        total = 0
        for hash, lenses in self.boxes.items():
            for idx, label in enumerate(lenses.keys()):
                total += (hash + 1) * (idx + 1) * lenses[label]
        return total


def s1(text: list) -> int:
    return sum([compute_hash(s) for s in text[0].split(",")])


def s2(text: list) -> int:
    boxes = Boxes()
    for s in text[0].split(","):
        boxes.process_step(s)
    return boxes.power()


print(s1(text))
print(s2(text))
