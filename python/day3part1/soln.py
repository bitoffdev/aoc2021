from collections import Counter
import sys


def mode(arr):
    return sum(map(lambda item: Counter({item: 1}), arr), Counter()).most_common()[0][0]


# fh = open("sample.in")
fh = sys.stdin

lines = fh.read().strip().split("\n")

transpose = [
    [lines[i][j] for i in range(len(lines))]
    for j in range(len(lines[0]))
]

gamma_rate = ''.join(mode(r) for r in transpose)
epsilon_rate = ''.join({'0': '1', '1': '0'}[b] for b in gamma_rate)
power_consumption = int(gamma_rate, base=2) * int(epsilon_rate, base=2)

print(power_consumption)

