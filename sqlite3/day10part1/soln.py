from collections import deque
import sys


syntax_error_score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
opening = "([{<"
closing = ")]}>"


def find_first_corrupt_char(line):
    q = deque()
    for i, c in enumerate(line):
        if c in opening:
            q.append(c)
        else:
            pop = q.pop()
            if opening.index(pop) != closing.index(c):
                return c
    return None


total = 0
for line in sys.stdin:
    c = find_first_corrupt_char(line.strip())
    if c:
        total += syntax_error_score_table[c]
print(total)

