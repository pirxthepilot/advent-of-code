with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]


def gen_ids(assigned: str) -> set:
    first, last = assigned.split("-")
    ids = set()
    for item in range(int(first), int(last)+1):
        ids.add(str(item))
    return ids


total_dupes = 0
for pair in text:
    left, right = [gen_ids(i) for i in pair.split(",")]
    if (
        left.issubset(right) or
        right.issubset(left)
    ):
        total_dupes += 1

answer_1 = total_dupes


total_overlaps = 0
for pair in text:
    left, right = [gen_ids(i) for i in pair.split(",")]
    if not left.isdisjoint(right):
        total_overlaps += 1

answer_2 = total_overlaps


print(answer_1)
print(answer_2)
