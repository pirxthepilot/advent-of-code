from __future__ import annotations
from collections import deque
from typing import List, Optional, Union

import re


class File:
    def __init__(
        self,
        name: str,
        size: Optional[int] = 0,
    ):
        self.name = name
        self.size = size
        self.parent: Optional[dir] = None

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, size={self.size})"

    def __str__(self):
        return self.name

    def __eq__(self, other: File):
        if (
            self.name == other.name and
            self.size == other.size and
            (
                (self.parent is None and other.parent is None) or
                (self.parent and other.parent and self.parent == other.parent)
            )
        ):
            return True
        return False

    def set_parent(self, parent_dir: Dir) -> None:
        self.parent = parent_dir


class Dir(File):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[Union[File, Dir]] = []

    @property
    def total_size(self):
        return sum([c.size for c in self.children])

    def add_child(self, child: Union[File, Dir]) -> None:
        child.set_parent(self)
        self.children.append(child)

    def get_child_by_name(self, name: str):
        for c in self.children:
            if str(c) == name:
                return c

    def get_all_dirs(self):
        # Do BFS
        visited = []
        queue = deque()

        queue.append(self)
        while queue:
            current = queue.popleft()
            visited.append(current)
            for c in current.children:
                if (
                    isinstance(c, Dir) and
                    c not in visited
                ):
                    queue.append(c)
        return visited

    def get_recursive_total_size(self):
        return sum([c.total_size for c in self.get_all_dirs()])

    def report_all_dir_sizes(self):
        report = {}
        for c in self.get_all_dirs():
            key = f"{c.parent.name}/{c.name}" if c.parent else f"{c.name}"
            report[key] = c.get_recursive_total_size()
        return report

    def tree(self) -> None:
        for child in self.children:
            if isinstance(child, Dir):
                child.tree()
            else:
                print(f"{child.size} {child.name}")


# with open("test.txt") as f:
with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]

cmd_re = re.compile(r"\$ (?P<cmd>[a-z]+)\s?(?P<arg>\S*)")
root = Dir("/")
current = root
for line in text:
    cmd = cmd_re.match(line)
    if cmd:  # Command was run
        cmd, arg = cmd.groups()
        if cmd == "cd" and arg != "/":
            if arg != "..":
                changedir = Dir(arg)
                changedir.set_parent(current)
                if changedir not in current.children:
                    current = current.add_child(changedir)
                current = current.get_child_by_name(changedir.name)
            else:
                current = current.parent
    else:    # Output was shown
        size, name = line.split(" ")
        if size == "dir":
            current.add_child(Dir(name))
        else:
            current.add_child(File(name, int(size)))

# root.tree()
# print(root.get_all_dirs())
# print(root.report_all_dir_sizes())


# Part 1

total = 0
for dir_, size in root.report_all_dir_sizes().items():
    if size <= 100000:
        total += size

answer_1 = total
print(answer_1)


# Part 2

total_disk_space = 70000000
required_space = 30000000
current_used_space = root.get_recursive_total_size()

deletion_candidate = []
for dir_, size in root.report_all_dir_sizes().items():
    if (current_used_space - size) + required_space <= total_disk_space:
        deletion_candidate.append((dir_, size))

answer_2 = min([c[1] for c in deletion_candidate])

print(deletion_candidate)
print(answer_2)
