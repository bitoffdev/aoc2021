from collections import deque
from contextlib import suppress
from statistics import median
import sys


part2_table = dict(zip(")]}>",range(1,5)))
opening = "([{<"
closing = ")]}>"


class CorruptLine(Exception):
    def __init__(self, c):
        self.bad_char = c


def get_completion(line):
    q = deque()
    for i, c in enumerate(line):
        if c in opening:
            q.append(c)
        else:
            pop = q.pop()
            if opening.index(pop) != closing.index(c):
                raise CorruptLine(c)
    return ''.join(
        closing[opening.index(c)]
        for c in q
    )[::-1]


def score_completion(completion):
    score = 0
    for c in completion:
       score = score * 5 + part2_table[c]
    return score


def main():
    scores = []
    for line in sys.stdin:
        with suppress(CorruptLine):
            scores.append(score_completion(get_completion(line.strip())))
    print(median(scores))


if __name__ == "__main__":
    main()
