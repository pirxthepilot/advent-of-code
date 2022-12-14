from __future__ import annotations

import abc
import os
from dataclasses import dataclass
from time import sleep
from typing import List, Optional, Tuple


@dataclass
class Location:
    x: int
    y: int


@dataclass
class Object(abc.ABC):
    loc: Location


@dataclass
class Rock(Object):
    sprite: str = "#"


@dataclass
class Sand(Object):
    world: World
    sprite: str = "o"
    settled: bool = False

    def update(self, include_floor=False) -> None:
        if self.settled:
            return

        if include_floor:
            if self.loc.y+1 == self.world.rocks_max_y + 2:
                self.settled = True
                return

        bottom = Location(self.loc.x, self.loc.y+1)
        bottomleft = Location(self.loc.x-1, self.loc.y+1)
        bottomright = Location(self.loc.x+1, self.loc.y+1)

        if not self.world.object_exists(bottom):
            self.loc = bottom
        elif not self.world.object_exists(bottomleft):
            self.loc = bottomleft
        elif not self.world.object_exists(bottomright):
            self.loc = bottomright
        else:  # No more space to move
            self.settled = True


class World:
    sand_src = Location(500, 0)

    def __init__(self):
        self.objects = []
        self.sand_ctr = 0
        self.current_sand = self._new_sand()
        self.rocks_max_y = None

    def _new_sand(self) -> Sand:
        sand = Sand(loc=self.sand_src, world=self)
        self.objects.append(sand)
        self.sand_ctr += 1
        return sand

    def add_rock(self, rock: Rock) -> None:
        if rock not in self.objects:
            self.objects.append(rock)

    def process_rocks(self, coords: List[Tuple[int, int]]) -> None:
        for idx in range(1, len(coords)):
            x1, y1 = coords[idx]
            x0, y0 = coords[idx-1]
            if x1 == x0:
                step = 1 if y0 <= y1 else -1
                for y in range(y0, y1 + step, step):
                    self.add_rock(Rock(Location(x1, y)))
            elif y1 == y0:
                step = 1 if x0 <= x1 else -1
                for x in range(x0, x1 + step, step):
                    self.add_rock(Rock(Location(x, y1)))

        self.rocks_max_y = max([o.loc.y for o in self.objects if isinstance(o, Rock)])

    def object_exists(self, loc: Location) -> bool:
        return loc in [o.loc for o in self.objects]

    def get_object(self, x: int, y: int) -> Optional[Location]:
        loc = Location(x, y)
        for o in self.objects:
            if o.loc == loc:
                return o
        return None

    def update(self, include_floor=False) -> None:
        if self.current_sand.settled is True:
            self.current_sand = self._new_sand()
        else:
            self.current_sand.update(include_floor)

    def draw(self) -> None:
        min_x = min([o.loc.x for o in self.objects])
        max_x = max([o.loc.x for o in self.objects])
        max_y = max([o.loc.y for o in self.objects])

        for y in range(0, max_y+1):
            row = ""
            for x in range(min_x, max_x+1):
                obj = self.get_object(x, y)
                if obj:
                    row += obj.sprite
                else:
                    row += "."
            print(row)

        print(f"\nSand: {self.sand_ctr}")


with open("test.txt") as f:
# with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]


def new_world() -> World:
    world = World()
    for line in text:
        coords = []
        for coord in line.split(" -> "):
            x, y = coord.split(",")
            coords.append((int(x), int(y)))

        world.process_rocks(coords)
    return world


# Part 1

w1 = new_world()
while w1.current_sand.loc.y <= max([o.loc.y for o in w1.objects[:-1]]) + 2:
    # os.system("cls")
    # w1.draw()
    w1.update()
    # sleep(0.05)

w1.draw()

answer_1 = w1.sand_ctr - 1
print(f"Rested sand: {answer_1}")


# Part 2

w2 = new_world()

while not (
    w2.current_sand.settled and
    w2.current_sand.loc == w2.sand_src
):
    # os.system("cls")
    # w2.draw()
    w2.update(include_floor=True)
    # print(f"{w2.sand_ctr} : {len(w2.objects)}")
    # sleep(0.02)

w2.draw()

answer_2 = w2.sand_ctr
print(f"Sand no longer spawns after {answer_2} sand!")
