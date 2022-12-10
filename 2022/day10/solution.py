import os
from collections import deque
from copy import deepcopy


class Instruction:
    def __init__(self, op, val=None):
        self.op = op
        self.val = int(val) if val else None
        self.timer = self._compute_runtime()

    def _compute_runtime(self):
        if self.op == "addx":
            return 2
        elif self.op == "noop":
            return 1
        else:
            raise Exception


class CrtCircuit:
    def __init__(self, instructions: deque):
        self.register = 1
        self.instructions = instructions
        self.current_op: Instruction = None

    def _process_op(self):
        if self.current_op is None:
            self.current_op = self.instructions.popleft()
        self.current_op.timer -= 1

    def _exec(self):
        if self.current_op.timer == 0:
            if self.current_op.op == "addx":
                self.register += self.current_op.val
            elif self.current_op.op == "noop":
                pass
            self.current_op = None

    def signal_strength(self):
        samples = {k: 0 for k in [20, 60, 100, 140, 180, 220]}
        cycles = max([k for k in samples.keys()])

        for tick in range(1, cycles + 1):
            # start processing op
            self._process_op()

            # sampling
            if tick in samples.keys():
                # print(f"SAMPLE: {tick}: {self.register}")
                samples[tick] = self.register

            # exec op if applicable
            self._exec()

        # Calculate signal strength
        strength = 0
        for tick, value in samples.items():
            strength += tick * value
        return strength

    def render(self):
        cycles = 240
        screen_width = 40
        display = ""

        for tick in range(1, cycles + 1):
            # start processing op
            self._process_op()

            # Draw
            pixel_idx = tick - 1
            sprite_loc = [self.register - 1, self.register, self.register + 1]

            # print(f"pixel: {pixel_idx} sprites: {sprite_loc}")
            if pixel_idx % screen_width in sprite_loc:
                display += "#"
            else:
                display += "."
            if tick % screen_width == 0:
                display += os.linesep

            # exec op if applicable
            self._exec()

        return display


instructions = deque()
# with open("test.txt") as f:
with open("input.txt") as f:
    for line in f.readlines():
        op, val = line.strip().split(" ") if " " in line else (line.strip(), "")
        instructions.append(Instruction(op, val))


# Part 1

crt = CrtCircuit(deepcopy(instructions))
print(crt.signal_strength())


# Part 2
print()
crt2 = CrtCircuit(deepcopy(instructions))
print(crt2.render())
