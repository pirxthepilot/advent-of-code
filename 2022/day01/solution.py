with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]

stash = [0]
for line in text:
    if line == "":
        stash.append(0)
    else:
        stash[-1] += int(line)

part1_answer = max(stash)

sum_ = 0
for num in sorted(stash, reverse=True)[0:3]:
    sum_ += num

part2_answer = sum_

print(part1_answer)
print(part2_answer)
