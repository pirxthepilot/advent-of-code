from dataclasses import dataclass
from itertools import permutations
from typing import Set, Tuple


@dataclass
class Cube:
    def __init__(self, x: int, y: int, z: int):
        self.pos = (x, y, z)

        # Neighbors
        self.sides = set([
            (x, y+1, z),  # top
            (x, y-1, z),  # bottom
            (x-1, y, z),  # left
            (x+1, y, z),  # right
            (x, y, z+1),  # back
            (x, y, z-1),  # front
        ])

        # Exposed sides
        self.exposed = 6
    
    def __repr__(self):
        return f"Cube({self.pos})"


cubes = []
# with open("test.txt") as f:
with open("input.txt") as f:
    for line in [l.strip() for l in f.readlines()]:
        x, y, z = line.split(",")
        cubes.append(Cube(int(x), int(y), int(z)))


# Part 1

for combo in permutations(cubes, r=2):
    c1, c2 = combo
    if c2.pos in c1.sides:
        c1.exposed -= 1

answer_1 = sum([c.exposed for c in cubes])
print(answer_1)
