from functools import reduce
import sys

DIGIT_SEGMENTS = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'},
}


def read_entry(line):
    raw_signal_patterns, raw_output_patterns = line.split('|')
    return (
        raw_signal_patterns.split(),
        raw_output_patterns.split(),
    )


# fh = open('sample.in')
fh = sys.stdin
entries = [
    read_entry(line)
    for line in fh
]

print(sum(
    1
    for cnt in (
        len(pattern)
        for pattern in reduce(
            lambda a, b: a + b,
            (
                entry[1]
                for entry in entries
            ),
        )
    )
    if cnt in [
        len(DIGIT_SEGMENTS[x])
        for x in [1,4,7,8]
    ]
))
