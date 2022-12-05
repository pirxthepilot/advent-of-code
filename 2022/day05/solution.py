import re
import os
from typing import Tuple


with open("input.txt") as f:
    text = [t.strip(os.linesep) for t in f.readlines()]
    #text = f.readlines()

instructions = text[10:]


class Stacks:
    instruction_re = re.compile(r"move (?P<qty>\d+) from (?P<src>\d) to (?P<dest>\d)")

    def __init__(self):
        self.stacks = {}
        for i in range(1, 10):
            self.stacks[i] = []
    
    def _move(self, qty: int, src: int, dest: int) -> None:
        for _ in range(qty):
            self.stacks[dest].append(self.stacks[src].pop())
    
    def _move_v2(self, qty: int, src: int, dest: int) -> None:
        buffer = []
        for _ in range(qty):
            buffer.append(self.stacks[src].pop())
        buffer.reverse()
        self.stacks[dest] += buffer
    
    def _parse_instruction(self, instruction: str) -> Tuple:
        parsed = self.instruction_re.match(instruction)
        if parsed:
            return parsed.groups()
        else:
            raise Exception("Broken regex")
    
    def run_instruction(self, instruction: str) -> None:
        qty, src, dest = self._parse_instruction(instruction)
        self._move(int(qty), int(src), int(dest))
    
    def run_instruction_v2(self, instruction: str) -> None:
        qty, src, dest = self._parse_instruction(instruction)
        # print(f"Move {qty} from {self.stacks[int(src)]} to {self.stacks[int(dest)]}")
        self._move_v2(int(qty), int(src), int(dest))
        # print(f"  Result: {self.stacks[int(src)]} : {self.stacks[int(dest)]}")
    
    def get_top_crates(self):
        answer = ""
        for key, stack in self.stacks.items():
            answer += stack[-1]
            print(f"{key}: {stack[-1]}")
        return answer


def init_stacks():
    s = Stacks()
    # Configure initial state
    for layer in text[7::-1]:
        stack_idx = 1
        for idx in range(1, 35, 4):
            if not layer[idx] == " ":
                s.stacks[stack_idx].append(layer[idx])
            stack_idx += 1
    return s


## Part 1

s = init_stacks()

# Run instructions
for instruction in instructions:
    s.run_instruction(instruction)

answer_1 = s.get_top_crates()
print(answer_1)


## Part 2

s2 = init_stacks()

# Run instructions
for instruction in instructions:
    s2.run_instruction_v2(instruction)

answer_2 = s2.get_top_crates()
print(answer_2)
