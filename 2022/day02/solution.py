with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]

shape = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}


def outcome(line):
    if line in ["A X", "B Y", "C Z"]:
        return 3
    elif line in ["A Y", "B Z", "C X"]:
        return 6
    else:
        return 0

score = 0
for line in text:
    score += shape[line[2]] + outcome(line)

p1_answer = score


idx = {k: v for v, k in enumerate(["A", "B", "C"])}
new_shape = {
    "A": 1,
    "B": 2,
    "C": 3,
}
def new_outcome(line):
    them, expected = tuple(line.split(" "))
    pointer = idx[them]
    if expected == "X":  # lose
        me = "ABC"[(pointer-1)%3]
        return new_shape[me]
    elif expected == "Y": # draw
        me = them
        return new_shape[me] + 3
    else:  # win
        me = "ABC"[(pointer+1)%3]
        return new_shape[me] + 6
    


new_score = 0
for line in text:
    #new_score += new_outcome(line)
    new_score += new_outcome(line)

p2_answer = new_score

print(p1_answer)
print(p2_answer)
