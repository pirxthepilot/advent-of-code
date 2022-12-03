from string import ascii_lowercase, ascii_uppercase

with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]

def get_priority(thing):
    for idx, item in enumerate(ascii_lowercase + ascii_uppercase):
        if thing == item:
            return idx+1


priority = 0
for rucksack in text:
    c1 = set()
    c2 = set()
    for idx, item in enumerate(rucksack):
        if idx < len(rucksack)/2:
            c1.add(item)
        else:
            c2.add(item)
    common = c1.intersection(c2).pop()
    priority += get_priority(common)


answer_1 = priority


groups = []
for idx, rucksack in enumerate(text):
    if idx % 3 == 0:
        current_group = [set(rucksack)]
        groups.append(current_group)
    else:
        groups[-1].append(set(rucksack))


priority = 0
for group in groups:
    common = group[0].intersection(group[1]).intersection(group[2])
    priority += get_priority(common.pop())


answer_2 = priority

print(answer_1)
print(answer_2)
