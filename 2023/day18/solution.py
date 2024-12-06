import sys
from typing import List, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


class Map:
    def __init__(self, plan: list):
        (self.trenches,
         self.first_x,
         self.first_y,
         self.last_x,
         self.last_y) = self._process(plan)

    @staticmethod
    def _process(plan: list) -> List[Tuple[int, int, str]]:
        trenches = {(0, 0): ""}
        first_x, first_y, last_x, last_y = (0, 0, 0, 0)

        for step in plan:
            dir, meters, color = step
            prev_x, prev_y = list(trenches.keys())[-1]
            x, y = prev_x, prev_y
            move_x, move_y = None, None

            if dir == "U":
                move_y = -int(meters)
            elif dir == "R":
                move_x = int(meters)
            elif dir == "D":
                move_y = int(meters)
            elif dir == "L":
                move_x = -int(meters)

            if move_x:
                inc = int(move_x/abs(move_x))
                for x in range(prev_x + inc, prev_x + move_x + inc, inc):
                    trenches[(x, y)] = color
            elif move_y:
                inc = int(move_y/abs(move_y))
                for y in range(prev_y + inc, prev_y + move_y + inc, inc):
                    trenches[(x, y)] = color

            if x < first_x:
                first_x = x
            if y < first_y:
                first_y = y
            if x > last_x:
                last_x = x
            if y > last_y:
                last_y = y

        return trenches, first_x, first_y, last_x, last_y

    def _fill(self) -> None:
        for y in range(self.first_y, self.last_y + 1):
            for x in range(self.first_x, self.last_x + 1):
                pass

    def draw(self) -> None:
        for y in range(self.first_y, self.last_y + 1):
            for x in range(self.first_x, self.last_x + 1):
                if (x, y) in self.trenches:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


with open(FILE, "r") as f:
    m = Map([t.strip().split(" ") for t in f.readlines()])

m.draw()
