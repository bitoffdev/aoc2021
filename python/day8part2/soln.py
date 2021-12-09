from dataclasses import dataclass
from functools import reduce
import itertools
# coding: utf-8
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
def get_possible_segments(cnt):
    return reduce(
        lambda a, b: a | b,
        (
            segments
            for segments in DIGIT_SEGMENTS.values()
            if len(segments) == cnt
        ),
        set()
    )


def get_impossible_segments(cnt):
    # Ignore the function name. It's bs.
    possible_segments = [
        segments
        for segments in DIGIT_SEGMENTS.values()
        if len(segments) == cnt
    ]
    if len(possible_segments) == 1:
        return possible_segments[0]
    return set()


@dataclass
class State:
    # Store possible mappings from each signal to each segment
    signal2segment: dict
    # Store possible mappings from each pattern to a digit
    pattern2digit: dict
    @classmethod
    def from_patterns(cls, patterns):
        return cls(
            signal2segment = {
                k: set('abcdefg')
                for k in 'abcdefg'
            },
            pattern2digit = {
                k: set(range(10))
                for k in patterns
            }
        )


def opt1(s):
    possibility_matrix = s.signal2segment

    for pattern in entry[0]:
        # Find all the possible segments given the length of the pattern.
        possible_segments = get_possible_segments(len(pattern))
        for letter in pattern:
            possibility_matrix[letter] &= possible_segments

        # When we know *exactly* which digit this pattern represents,
        # we can update letters missing from this pattern to reflect
        # that they may not use the segments making up the known digit.
        impossible_segments = get_impossible_segments(len(pattern))
        for letter in set('abcdefg') - set(pattern):
            possibility_matrix[letter] -= impossible_segments
        # TODO This is roughly the same idea as above. Deduplicate
        digits = s.pattern2digit[pattern]
        if len(digits) == 1:
            for letter in set('abcdefg') - set(pattern):
                possibility_matrix[letter] -= DIGIT_SEGMENTS[next(iter(digits))]


def opt2(s):
    possibility_matrix = s.signal2segment
    pattern_possibility_matrix = s.pattern2digit
    for pattern, digits in pattern_possibility_matrix.items():
        available_segments = reduce(
            lambda a, b: a | b,
            (
            possibility_matrix[signal]
            for signal in pattern
            ),
            set()
        )

        for digit in list(digits):
            if (
                len(DIGIT_SEGMENTS[digit]) == len(pattern) and
                DIGIT_SEGMENTS[digit].issubset(available_segments)
            ):
                pass
            else:
                pattern_possibility_matrix[pattern] -= {digit}


def opt3(s):
    possibility_matrix = s.signal2segment
    pattern_possibility_matrix = s.pattern2digit
    for pattern, digits in pattern_possibility_matrix.items():
        # Given the signal pattern, figure out what segment
        # patterns are possible using all the mappings that
        # we currently think are possible
        possible_segments = [
            set(x)
            for x in itertools.product(
                *[s.signal2segment[signal]
                for signal in pattern]
            )
        ]


        for digit in list(digits):
            if (
                DIGIT_SEGMENTS[digit] in possible_segments
            ):
                pass
            else:
                pattern_possibility_matrix[pattern] -= {digit}


def opt4(s):
    # If we have "locked in" some signal-to-segment mappings (ie. we have a one-to-one)
    # then remove the LHS from other mappings.
    for signal in 'abcdefg':
        if len(s.signal2segment[signal]) == 1:
            for other_signal in (set('abcdefg') - {signal}):
                s.signal2segment[other_signal] -= s.signal2segment[signal]


def micropass(s):
    # The number of iterations, 5, was chosen at random, but I do think that a
    # few iterations could be necessary.
    for _ in range(5):
        opt1(s)
        opt2(s)
        opt3(s)
        opt4(s)


def get_output_value(entry):
    s = State.from_patterns(entry[0] + entry[1])
    micropass(s)
    return int("".join(
        str(next(iter(s.pattern2digit[pattern])))
        for pattern in entry[1]
    ))




import sys
entries = [
    read_entry(line)
    for line in sys.stdin
]

total = 0
for entry in entries:
    entry_value = get_output_value(entry)
    total += entry_value

print(total)
