from sys import stdin

count = 0


window = []

for i in range(3):
    line = next(stdin)
    num = int(line.strip())
    window.append(num)


for line in stdin:
    previous = sum(window)
    window.pop(0)
    num = int(line.strip())
    window.append(num)
    current = sum(window)
    if previous is not None and current > previous:
        count += 1

print(count)
