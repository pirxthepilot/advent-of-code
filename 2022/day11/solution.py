from __future__ import annotations

import operator
import re
from collections import deque
from math import floor


class Monkey:
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
    }

    def __init__(
        self,
        id_: int,
        starting_items: deque,
        op_params: list = [],
        test_divisible_by: int = 0,
        test_true_dest: Monkey = None,
        test_false_dest: Monkey = None,
    ):
        self.id_ = id_
        self.loot = starting_items
        self.op_params = op_params
        self.divisible_by = test_divisible_by
        self.true_dest = test_true_dest
        self.false_dest = test_false_dest
        self.items_inspected = 0

    def __str__(self):
        return (f"Monkey({self.id_}, loot={self.loot}, op={self.op_params}, "
                f"test={self.divisible_by}, true={self.true_dest}, false={self.false_dest})")

    def _do_operation(self, item, base_multiple):
        operation, op1, op2 = self.op_params
        op1 = item if op1 == "old" else int(op1)
        op2 = item if op2 == "old" else int(op2)
        # Normalize to base_multiple
        return self.ops[operation](op1, op2) % base_multiple

    def _test(self, item):
        return True if item % self.divisible_by == 0 else False

    def start(self, base_multiple, no_relief=False):
        """ Start inspection and throw items """
        while self.loot:
            # Grab next item
            item = self.loot.popleft()

            # Increment score
            self.items_inspected += 1

            # Do the operation
            item = self._do_operation(item, base_multiple)

            # Relief
            if no_relief is False:
                item = floor(item/3)

            # Test and throw
            if self._test(item):
                yield (self.true_dest, item)
            else:
                yield (self.false_dest, item)


class Monkeys:
    def __init__(self):
        self.monkeys = []

    def add(self, monkey: Monkey):
        self.monkeys.append(monkey)

    def get_monkey(self, id_):
        for m in self.monkeys:
            if m.id_ == id_:
                return m

    def print_stats(self):
        for m in self.monkeys:
            print(f"Monkey {m.id_}: {m.items_inspected} items inspected ({list(m.loot)})")

    def top_two(self):
        top1, top2 = sorted([m.items_inspected for m in self.monkeys], reverse=True)[:2]
        return top1 * top2

    def _get_base_multiple(self):
        multiple = 1
        for m in self.monkeys:
            multiple *= m.divisible_by
        return multiple

    def start(self, rounds: int = 1, no_relief: bool = False):
        base_multiple = self._get_base_multiple()
        for _ in range(rounds):
            for m in self.monkeys:
                for thrown in m.start(base_multiple, no_relief):
                    dest, item = thrown
                    dest = self.get_monkey(dest)
                    dest.loot.append(item)


# with open("test.txt") as f:
with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]


# Messy conversion
def fresh_data():
    monkeys = Monkeys()
    for line in text:
        if line.startswith("Monkey"):
            id_ = re.match(r"Monkey (?P<id_>\d+):", line).group("id_")
        elif line.strip().startswith("Starting items:"):
            starting_items = deque([int(i) for i in line.split(": ")[1].split(", ")])
        elif line.strip().startswith("Operation:"):
            op1, oper, op2 = re.search(r"new = (\S+) (\S+) (\S+)", line).groups()
            operation = (oper, op1, op2)
        elif line.strip().startswith("Test:"):
            test = re.search(r"Test: divisible by (?P<test>\d+)", line).group("test")
        elif line.strip().startswith("If "):
            result, dest_id = re.search(r"If (true|false): throw to monkey (\d+)", line).groups()
            if result == "true":
                true_dest_id = dest_id
            else:
                false_dest_id = dest_id
                monkeys.add(
                    Monkey(
                        int(id_),
                        starting_items,
                        operation,
                        int(test),
                        int(true_dest_id),
                        int(false_dest_id),
                    )
                )
    return monkeys


# Part 1

m1 = fresh_data()
m1.start(20)
m1.print_stats()
answer_1 = m1.top_two()
print(answer_1)


# Part 2

m2 = fresh_data()
m2.start(10000, no_relief=True)
m2.print_stats()
answer_2 = m2.top_two()
print(answer_2)
