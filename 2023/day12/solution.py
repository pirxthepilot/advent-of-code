import sys
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


def permutations(length: int) -> list:
    permutations = []

    queue = deque([["."], ["#"]])

    while queue:
        path = queue.popleft()
        if len(path) == length:
            permutations.append("".join(path))
            continue
        new_path = path
        queue.append(new_path + ["."])
        queue.append(new_path + ["#"])

    return permutations


@dataclass
class Row:
    parts: str
    cond: Tuple[int]
    
    def __repr__(self) -> str:
        return f"{self.parts} {self.cond}"
    
    def matches_condition(self, parts: str) -> bool:
        if "?" in parts:
            raise Exception(f"Invalid character: {c}")

        conds = deque(self.cond)
        current_count = 0
        current_cond = conds.popleft()
        for c in parts:
            if c == "#":
                if (
                    current_cond is None or
                    current_count >= current_cond
                ):
                    return False
                current_count += 1
                continue
            if current_count > 0:  # End contiguous group
                if current_count != current_cond:
                    return False
                current_count = 0
                current_cond = conds.popleft() if conds else None
        if current_count > 0:
            if current_count != current_cond:
                return False
            if conds:
                return False
        if (
            current_count == 0 and
            current_cond is not None
        ):
            return False

        return True


class Field:
    def __init__(self, text: List[str]):
        self.rows: List[Row] = []

        for line in text:
            parts, cond = line.split(" ")
            self.rows.append(Row(
                parts,
                tuple(int(c) for c in cond.split(","))
            ))
        
        self._pcache: Dict[int, List[str]] = {}  # Permutation cache
    
    def _get_permutations(self, length: int) -> List[str]:
        if length not in self._pcache:
            self._pcache[length] = permutations(length)
        return self._pcache[length]
    
    @staticmethod
    def _gen_replace_map(broken_idx: List[int], permutation: str) -> Dict[int, str]:
        replace_map = {}
        for idx, part in enumerate(permutation):
            replace_map[broken_idx[idx]] = part
        return replace_map
    
    def _find_arrangements(self, row: Row) -> int:
        # Get index of parts that are ?
        broken_idx = [i for i, c in enumerate(row.parts) if c == "?"]

        # Generate possible values to substitute to ?
        permutations = self._get_permutations(len(broken_idx))

        matches = 0
        for value in permutations:
            # Replace ?s with each possible value
            replaced = ""
            replace_map = self._gen_replace_map(broken_idx, value)
            for idx, part in enumerate(row.parts):
                if idx in replace_map:
                    replaced += replace_map[idx]
                else:
                    replaced += part
            # Check if replaced matches condition
            if row.matches_condition(replaced):
                matches += 1
                # print(f"{replaced} matches {row.cond}") 
        return matches
    
    def get_total_arrangements(self) -> int:
        sum = 0
        for row in self.rows:
            sum += self._find_arrangements(row)
        return sum


def s1(field: Field) -> int:
    return field.get_total_arrangements()


field = Field(text)
print(s1(field))
