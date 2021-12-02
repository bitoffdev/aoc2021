import sys

aim = 0
depth = 0
horiz = 0

for line in sys.stdin:
    action, value = line.strip().split()
    value = int(value)
    if action == 'forward':
        horiz += value
        depth += aim * value
    elif action == 'down':
        aim += value
    elif action == 'up':
        aim -= value
    else:
        raise Exception("Unexpected line: {}", line)

print(horiz * depth)
