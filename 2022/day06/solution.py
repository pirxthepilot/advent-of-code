from collections import deque


with open("input.txt") as f:
    text = f.read()


def detect_start_of(text: str, buffer_length: int) -> int:
    buffer = deque()
    for idx, c in enumerate(text):
        buffer.append(c)
        if len(buffer) == buffer_length + 1:
            buffer.popleft()
            if len(buffer) == len(set(buffer)):  # Detect repetition
                return idx + 1


def gen_test():
    return (
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    )


# Part 1
def detect_start_of_packet(text):
    return detect_start_of(text, 4)


for test in gen_test():
    print(detect_start_of_packet(test))


answer_1 = detect_start_of_packet(text)
print(f"ANSWER 1: {answer_1}")


# Part 2
def detect_start_of_message(text):
    return detect_start_of(text, 14)


for test in gen_test():
    print(detect_start_of_message(test))


answer_2 = detect_start_of_message(text)
print(f"ANSWER 2: {answer_2}")
