# coding: utf-8
from collections import Counter
import sys


def counts(arr):
    return sum(map(lambda item: Counter({item: 1}), arr), Counter())


def mode(arr):
    return sum(map(lambda item: Counter({item: 1}), arr), Counter()).most_common()[0][0]


# fh = open("sample.in")
fh = sys.stdin
lines = fh.read().strip().split("\n")


candidates = lines.copy()
for column_index in range(len(lines[0])):
    if len(candidates) == 1:
        break
    
    zeds = [
        line
        for line in candidates
        if line[column_index] == '0'
    ]
    ones = [
        line
        for line in candidates
        if line[column_index] == '1'
    ]
    if len(zeds) <= len(ones):
        candidates = ones
    else:
        candidates = zeds
oxygen_generator_rating = candidates[0]


candidates = lines.copy()
for column_index in range(len(lines[0])):
    if len(candidates) == 1:
        break
    
    zeds = [
        line
        for line in candidates
        if line[column_index] == '0'
    ]
    ones = [
        line
        for line in candidates
        if line[column_index] == '1'
    ]
    if len(zeds) <= len(ones):
        candidates = zeds
    else:
        candidates = ones
co2_scrubber_rating = candidates[0]


life_support_rating = int(oxygen_generator_rating, base=2) * int(co2_scrubber_rating, base=2)
print(life_support_rating)
