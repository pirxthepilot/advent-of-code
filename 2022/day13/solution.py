import json


def compare(in1, in2):
    def inner_compare(left, right):
        for idx in range(max([len(left), len(right)])):
            try:
                lv = left[idx]
            except IndexError:
                return True
            try:
                rv = right[idx]
            except IndexError:
                return False

            if isinstance(lv, int) and isinstance(rv, int):
                if lv < rv:
                    return True
                elif lv > rv:
                    return False

            elif isinstance(lv, int) and isinstance(rv, list):
                result = inner_compare([lv], rv)
                if result is not None:
                    return result

            elif isinstance(lv, list) and isinstance(rv, int):
                result = inner_compare(lv, [rv])
                if result is not None:
                    return result

            else:
                result = inner_compare(lv, rv)
                if result is not None:
                    return result

    outcome = inner_compare(in1, in2)
    return outcome if outcome is not None else True


# with open("test.txt") as f:
with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]


# Part 1

groups = []
current_group = []
for line in text:
    if line:
        current_group.append(json.loads(line))
    else:
        groups.append(current_group)
        current_group = []
groups.append(current_group)

right_order_pairs = 0
for idx, group in enumerate(groups):
    result = compare(group[0], group[1])
    if result is True:
        right_order_pairs += idx + 1

answer_1 = right_order_pairs
print(answer_1)


# Part 2

packets = [[[2]], [[6]]]
for line in text:
    if line:
        packets.append(json.loads(line))

for i in range(len(packets)):
    for j in range(len(packets) - i - 1):
        if not compare(packets[j], packets[j+1]):
            packets[j], packets[j+1] = packets[j+1], packets[j]

divider_product = 1
for idx, packet in enumerate(packets, start=1):
    # print(f"{idx}: {packet}")
    if packet in ([[2]], [[6]]):
        divider_product *= idx

answer_2 = (divider_product)
print(answer_2)
