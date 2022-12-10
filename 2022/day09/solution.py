from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import List


CWD = Path(__file__).resolve().parent

# with open(CWD / "test2.txt") as f:
with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]


@dataclass
class Position:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


class Knot:
    def __init__(self, name: str, pos: Position):
        self.name = name
        self.pos = pos
        self.following: Knot = None
        self.visited: List[Position] = [deepcopy(self.pos)]

    def follow(self, knot: Knot):
        self.following = knot

    @property
    def _following_hitbox(self):
        return {
            Position(self.following.pos.x+1, self.following.pos.y),  # R
            Position(self.following.pos.x-1, self.following.pos.y),  # L
            Position(self.following.pos.x, self.following.pos.y+1),  # U
            Position(self.following.pos.x, self.following.pos.y-1),  # D
        }

    @property
    def _following_hitbox_extended(self):
        return {
            Position(self.following.pos.x+1, self.following.pos.y+1),  # UR
            Position(self.following.pos.x+1, self.following.pos.y-1),  # LR
            Position(self.following.pos.x-1, self.following.pos.y+1),  # UL
            Position(self.following.pos.x-1, self.following.pos.y-1),  # LL
        }

    @property
    def _hitbox(self):
        return {
            Position(self.pos.x+1, self.pos.y),    # R
            Position(self.pos.x-1, self.pos.y),    # L
            Position(self.pos.x, self.pos.y+1),    # U
            Position(self.pos.x, self.pos.y-1),    # D
            Position(self.pos.x+1, self.pos.y+1),  # UR
            Position(self.pos.x+1, self.pos.y-1),  # LR
            Position(self.pos.x-1, self.pos.y+1),  # UL
            Position(self.pos.x-1, self.pos.y-1),  # LL
        }

    def update(self):
        # Following is still within self's vicinity - do nothing
        if (
            self.following.pos == self.pos or
            self.following.pos in self._hitbox
        ):
            return None

        # Detect intersection; self will move to this position
        try:
            self.pos = self._following_hitbox.intersection(self._hitbox).pop()
        except KeyError:
            # Following moved diagonally; let the hitbox extend
            self.pos = self._following_hitbox_extended.intersection(self._hitbox).pop()
        self.visited.append(deepcopy(self.pos))


class Map:
    def __init__(self, num_knots: int):
        self.knots = [Knot("H", Position(0, 0))]
        for n in range(1, num_knots):
            knot = Knot(str(n), Position(0, 0))
            knot.following = self.knots[-1]
            self.knots.append(knot)

    def _update(self):
        for knot in self.knots[1:]:
            knot.update()

    def run_instruction(self, instruction: str):
        head = self.knots[0]
        direction, steps = instruction.split(" ")
        for _ in range(int(steps)):
            # print([(k.name, k.pos, k.following.name if k.following else None) for k in self.knots])
            if direction == "U":
                head.pos.y += 1
            elif direction == "R":
                head.pos.x += 1
            elif direction == "D":
                head.pos.y -= 1
            elif direction == "L":
                head.pos.x -= 1
            head.visited.append(deepcopy(head.pos))
            # from time import sleep
            # print("BEFORE")
            # self.print_map()
            # print()
            # sleep(0.7)
            self._update()
            # print("AFTER")
            # self.print_map()
            # print()
            # sleep(0.7)

    def positions_occupied_by_tail(self):
        return len(set(self.knots[-1].visited))

    def print_map(self):
        all_visited = []
        for knot in self.knots:
            all_visited += knot.visited
        visited_x = [i.x for i in all_visited]
        visited_y = [i.y for i in all_visited]
        min_x = min(visited_x)
        max_x = max(visited_x)
        min_y = min(visited_y)
        max_y = max(visited_y)

        for y in range(max_y, min_y-1, -1):
            line = ""
            for x in range(min_x, max_x+1):
                pos = Position(x, y)
                knot_in_pos = False
                for k in self.knots:
                    # print(f"pos: {pos}, knot: {k.name} {k.pos}")
                    if pos == k.pos:
                        line += k.name
                        knot_in_pos = True
                        break
                if not knot_in_pos:
                    if pos == Position(0, 0):
                        line += "s"
                    # elif pos in self.tail_visited:
                    #     line += "#"
                    else:
                        line += "."
                if x != max_x:
                    line += " "
            print(line)


# Part 1

m = Map(2)
for instruction in text:
    m.run_instruction(instruction)

# m.print_map()
answer_1 = m.positions_occupied_by_tail()
print(answer_1)


# Part 2

m2 = Map(10)
for instruction in text:
    m2.run_instruction(instruction)

# m2.print_map()
answer_2 = m2.positions_occupied_by_tail()
print(answer_2)
