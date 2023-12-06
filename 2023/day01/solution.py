with open("input.txt", "r") as f:
    text = [t.strip() for t in f.readlines()]


def s1(text):
    values = []
    for line in text:
        number = [c for c in line if c.isnumeric()]
        values.append(int(number[0] + number[-1]))

    return sum(values)


def s2(text):
    converted_lines = []
    mapping = {
        "one": "o1e",
        "two": "t2o",
        "three": "thr3",
        "four": "fo4r",
        "five": "fi5e",
        "six": "s6x",
        "seven": "se7en",
        "eight": "ei8ht",
        "nine": "ni9e",
    }

    for line in text:
        for word, num in mapping.items():
            line = line.replace(word, str(num))
        converted_lines.append(line)
    
    return s1(converted_lines)


print(s1(text))
print(s2(text))
