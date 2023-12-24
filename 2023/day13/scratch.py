from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Shape:
    l: int
    r: int
    l_side: str = ""
    r_side: str = ""

    def __eq__(self, other: Shape) -> bool:
        return (
            self.l == other.l and
            self.r == other.r
        )


def sol(a):
    queue = deque([Shape(0, len(a)-1)])
    visited = []
    finals = []

    while queue:
        shape = queue.popleft()
        if shape.l >= shape.r and shape.l_side:
            return shape
        if shape not in visited:
            print(f"Comparing {shape}")
            visited.append(shape)
            queue.append(Shape(shape.l, shape.r-1))
            queue.append(Shape(shape.l+1, shape.r))
            if a[shape.l] == a[shape.r]:
                new_l_side = shape.l_side + a[shape.l]
                new_r_side = shape.r_side + a[shape.r]
                if new_l_side == new_r_side:
                    # print("  Match")
                    queue.append(Shape(
                        shape.l+1,
                        shape.r-1,
                        new_l_side,
                        new_r_side
                    ))
            # else:
        
    print(finals)


a = [2,8,2,2,3,4,5,5,4,3,2]
print(sol([str(i) for i in a]))
