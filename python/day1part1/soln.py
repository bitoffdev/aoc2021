from sys import stdin

count = 0

previous = None

for line in stdin:
    num = int(line.strip())
    if previous is not None and num > previous:
        count += 1
    previous = num

print(count)
