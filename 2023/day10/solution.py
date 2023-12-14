from __future__ import annotations

import math
import sys
from typing import Optional


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Pipe:
    valid_connections = {
        "|": ("n", "s"),
        "-": ("w", "e"),
        "L": ("n", "e"),
        "J": ("n", "w"),
        "7": ("w", "s"),
        "F": ("e", "s"),
    }

    def __init__(self, shape: str, x: int, y: int):
        self.shape = shape
        self.x = x
        self.y = y
        self.n: Optional[Pipe] = None
        self.e: Optional[Pipe] = None
        self.s: Optional[Pipe] = None
        self.w: Optional[Pipe] = None
    
    def __repr__(self) -> str:
        return f"{self.shape} ({self.x}, {self.y})"

    @staticmethod
    def _opposite(direction: str) -> str:
        if direction == "n":
            return "s"
        if direction == "s":
            return "n"
        if direction == "e":
            return "w"
        if direction == "w":
            return "e"

    def set_neighbor(self, direction: str, other: Pipe) -> None:
        # Make sure the neighbor actually connects
        if self.shape == "S":
            valid_s_connections = {
                "n": ("7", "|", "F"),
                "e": ("J", "-", "7"),
                "s": ("J", "|", "L"),
                "w": ("F", "-", "L"),
            }
            if other.shape not in valid_s_connections[direction]:
                raise Exception("Invalid connection for S")
        else:
            if direction not in self.valid_connections[self.shape]:
                raise Exception("Invalid connection")

        # Connect self and other
        setattr(self, direction, other)
        other.set_neighbor(self._opposite(direction), self)
    
    def exit_dir(self, enter_dir: str) -> str:
        dir_1, dir_2 = self.valid_connections[self.shape]
        return dir_2 if enter_dir == dir_1 else dir_1
 

class Map:
    def __init__(self, text: str):
        cache = {}
        for y, line in enumerate(text):
            for x, tile in enumerate(line):
                if tile == ".":
                    continue

                pipe = Pipe(tile, x, y)
                cache[(x, y)] = pipe
                if tile == "S":
                    self.start = pipe
                
                # See if N and W can be connected
                for d, xy in (
                    ("n", (x, y-1)),
                    ("w", (x-1, y)),
                ):
                    neighbor = cache.get(xy)
                    if neighbor:
                        try:
                            pipe.set_neighbor(d, neighbor)
                        except:
                            # print(f"{pipe} cannot connect to {neighbor}")
                            pass

    def walk(self) -> int:
        current = self.start
        current_from = None
        steps = 0
        while current != self.start or steps == 0:
            # print(f"{steps}: {current}")
            # print(f"    #N {current.n} #E {current.e} #S {current.s} #W {current.w}")

            if current.shape == "S":
                for d in ("n", "e", "s", "w"):
                    potential_next = getattr(current, d)
                    if potential_next:
                        current = potential_next
                        current_from = current._opposite(d)
                        break
            else:
                exit = current.exit_dir(current_from)
                current = getattr(current, exit)
                current_from = current._opposite(exit)
            steps += 1
        return math.ceil(steps/2)


def s1(grid: Map) -> int:
    return grid.walk()


grid = Map(text)
print(s1(grid))
