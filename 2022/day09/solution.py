from copy import deepcopy
from dataclasses import dataclass


# with open("input.txt") as f:
with open("test2.txt") as f:
    text = [t.strip() for t in f.readlines()]


@dataclass
class Position:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


class Map:
    def __init__(self):
        self.head = Position(0, 0)
        self.tail = Position(0, 0)
        self.head_visited = [deepcopy(self.head)]
        self.tail_visited = [deepcopy(self.tail)]

    @property
    def _head_hitbox(self):
        return {
            Position(self.head.x+1, self.head.y),  # R
            Position(self.head.x-1, self.head.y),  # L
            Position(self.head.x, self.head.y+1),  # U
            Position(self.head.x, self.head.y-1),  # D
        }

    @property
    def _tail_hitbox(self):
        return {
            Position(self.tail.x+1, self.tail.y),    # R
            Position(self.tail.x-1, self.tail.y),    # L
            Position(self.tail.x, self.tail.y+1),    # U
            Position(self.tail.x, self.tail.y-1),    # D
            Position(self.tail.x+1, self.tail.y+1),  # UR
            Position(self.tail.x+1, self.tail.y-1),  # LR
            Position(self.tail.x-1, self.tail.y+1),  # UL
            Position(self.tail.x-1, self.tail.y-1),  # LL
        }

    def _update_tail(self):
        # Head is still within tail's vicinity - do nothing
        if (
            self.head == self.tail or
            self.head in self._tail_hitbox
        ):
            return None

        # Detect intersection; tail will move to this position
        self.tail = self._head_hitbox.intersection(self._tail_hitbox).pop()

    def run_instruction(self, instruction: str):
        direction, steps = instruction.split(" ")
        for _ in range(int(steps)):
            # print([str(i) for i in self.visited])
            if direction == "U":
                self.head.y += 1
            elif direction == "R":
                self.head.x += 1
            elif direction == "D":
                self.head.y -= 1
            elif direction == "L":
                self.head.x -= 1
            self.head_visited.append(deepcopy(self.head))
            # self.print_map()
            # print()
            # from time import sleep
            # sleep(0.6)
            self._update_tail()
            self.tail_visited.append(deepcopy(self.tail))
            # self.print_map()
            # print()
            # sleep(0.6)

    def positions_occupied_by_tail(self):
        return len(set(self.tail_visited))

    def print_map(self):
        visited_x = [i.x for i in self.head_visited + self.tail_visited]
        visited_y = [i.y for i in self.head_visited + self.tail_visited]
        min_x = min(visited_x)
        max_x = max(visited_x)
        min_y = min(visited_y)
        max_y = max(visited_y)

        for y in range(max_y, min_y-1, -1):
            line = ""
            for x in range(min_x, max_x+1):
                pos = Position(x, y)
                if pos == self.head:
                    line += "H"
                elif pos == self.tail:
                    line += "T"
                elif pos == Position(0, 0):
                    line += "s"
                elif pos in self.tail_visited:
                    line += "#"
                else:
                    line += "."
                if x != max_x:
                    line += " "
            print(line)


# Part 1

m = Map()
for instruction in text:
    m.run_instruction(instruction)

m.print_map()
answer_1 = m.positions_occupied_by_tail()
print(answer_1)
