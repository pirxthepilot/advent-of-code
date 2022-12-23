from abc import ABC
from collections import deque
from typing import Tuple


class Rock(ABC):
    shape: list
    width: int
    height: int

    def __init__(self, init_loc: Tuple[int, int]):
        ix, iy = init_loc
        self.loc = set()
        for part in self.shape:
            bx, by = part
            self.loc.add((ix + bx, iy + by))
        
        self.settled = False
    
    @property
    def highest_y(self):
        return min([p[1] for p in self.loc])
    
    def look_left(self) -> set:
        new = set()
        for p in self.loc:
            x, y = p
            new.add((x - 1, y))
        return new

    def look_right(self) -> set:
        new = set()
        for p in self.loc:
            x, y = p
            new.add((x + 1, y))
        return new

    def look_down(self) -> set:
        new = set()
        for p in self.loc:
            x, y = p
            new.add((x, y + 1))
        return new


class Prone(Rock):
    shape = [
        (0, 0), (1, 0), (2, 0), (3, 0),
    ]
    width = 4
    height = 1


class Cross(Rock):
    shape = [
                (1, 0),
        (0, 1), (1, 1), (2, 1),
                (1, 2),
    ]
    width = 3
    height = 3


class Lazy(Rock):
    shape = [
                        (2, 0),
                        (2, 1),
        (0, 2), (1, 2), (2, 2),
    ]
    width = 3
    height = 3


class Upright(Rock):
    shape = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
    ]
    width = 1
    height = 4


class Box(Rock):
    shape = [
        (0, 0), (1, 0),
        (0, 1), (1, 1),
    ]
    width = 2
    height = 2


class Chamber:
    rock_types = [Prone, Cross, Lazy, Upright, Box]

    def __init__(self, jet_pattern: str, init_y: int = 0):
        self.jet_pattern = deque(jet_pattern)
        self.settled = set()

        self.floor = init_y + self.rock_types[0].height + 4
        self.highest_y = self.floor
    
        self.left_wall_x = 0
        self.right_wall_x = 8

        self.next_rock_idx = 0
        self.rock_count = 0
        self.cur_rock = self._manifest()
    
    @property
    def tower_height(self):
        return self.floor - self.highest_y
    
    def _manifest(self):
        rock = self.rock_types[self.next_rock_idx]
        start_x = self.left_wall_x + 3
        start_y = self.highest_y - 3 - rock.height
        new_rock = rock((start_x, start_y))
        self.rock_count += 1
        self.next_rock_idx = (self.next_rock_idx + 1) % len(self.rock_types)
        return new_rock
    
    def _get_next_move(self):
        next = self.jet_pattern.popleft()
        self.jet_pattern.append(next)
        return next

    def _check_movement(self, move_func) -> None:
        new_loc = move_func()
        xs = set() 
        ys = set()
        for l in new_loc:
            x, y = l
            xs.add(x)
            ys.add(y)

        # Lateral movement
        # Touching other rocks or the wall
        if move_func.__name__ in ["look_left", "look_right"]:
            if (
                new_loc.isdisjoint(self.settled) and
                xs.isdisjoint(set([self.left_wall_x, self.right_wall_x]))
            ):
                self.cur_rock.loc = new_loc
        
            return

        # Downward movement
        # Touching other rocks or floor
        if (
            new_loc.isdisjoint(self.settled) and
            ys.isdisjoint(set([self.floor]))
        ):
            self.cur_rock.loc = new_loc
        else:
            # Add rock to settled
            self.settled.update(self.cur_rock.loc)
            self.highest_y = min([l[1] for l in self.settled])
            # New rock!
            self.cur_rock = self._manifest()
    
    def update(self) -> None:
        # Lateral movement
        movement = self._get_next_move()
        if movement == "<":
            self._check_movement(self.cur_rock.look_left)
        elif movement == ">":
            self._check_movement(self.cur_rock.look_right)
        else:
            raise SystemError(f"Invalid movement: {movement}")
        
        # Fall
        self._check_movement(self.cur_rock.look_down)

    def draw(self) -> None:
        min_y = min([self.highest_y, self.cur_rock.highest_y])

        for y in range(min_y, self.floor + 1):
            line = ""
            for x in range(self.left_wall_x, self.right_wall_x + 1):
                if y == self.floor:
                    line += "-"
                elif x in [self.left_wall_x, self.right_wall_x]:
                    line += "|"
                elif (x, y) in self.cur_rock.loc:
                    line += "@"
                elif (x, y) in self.settled:
                    line += "#"
                else:
                    line += "."
            print(line)


test_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

with open("input.txt") as f:
    input_pattern = f.read()

input_pattern = input_pattern.strip()


# Part 1

# c = Chamber(test_pattern)
# c = Chamber(input_pattern)
# from time import sleep
# import os
# while c.rock_count <= 2022:
#     # os.system("clear")
#     # c.draw()
#     # print(c.rock_count)
#     # sleep(0.3)
#     c.update()

# answer_1 = c.tower_height
# print(answer_1)


# Part 2

c2 = Chamber(test_pattern)
# c2= Chamber(input_pattern)
while c2.rock_count <= 1000000000000:
    c2.update()
    if c2.rock_count % 1000 == 0:
        print(c2.rock_count)

answer_2 = c2.tower_height
print(answer_2)
