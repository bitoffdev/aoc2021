import sys

depth = 0
horiz = 0

for line in sys.stdin:
    action, value = line.strip().split()
    value = int(value)
    if action == 'forward':
        horiz += value
    elif action == 'down':
        depth += value
    elif action == 'up':
        depth -= value
    else:
        raise Exception("Unexpected line: {}", line)

print(horiz * depth)
