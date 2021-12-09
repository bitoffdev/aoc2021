import sys

positions = [
    int(x)
    for x in sys.stdin.read().strip().split(",")
]

def cost(crab_positions, align_position: int):
    return sum(abs(p - align_position) for p in crab_positions)

pos2cost = {}
for pos in range(min(positions), max(positions) + 1):
    pos2cost[pos] = cost(positions, pos)

print(min(pos2cost.items(), key=lambda x: x[1])[1])
