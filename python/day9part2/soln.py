from collections import deque
from functools import reduce
import sys


def get_heightmap(fh):
    heightmap = {}
    for row, row_value in enumerate(fh):
        for col, col_value in enumerate(map(int, row_value.strip())):
            heightmap[row,col] = col_value
    return heightmap


def neighbors(row, col):
    return set(
        (row + row_offset, col + col_offset)
        for row_offset, col_offset in [(-1,0), (1,0), (0,-1), (0,1)]
    )


def scan_basin(heightmap, start, unvisited):
    q = deque([start])
    basin = set()
    while len(q) > 0:
        cur_pos = q.pop()
        unvisited -= {cur_pos}
        # visited.add(cur_pos)
        # skip if 9 or if out of bounds
        if heightmap.get(cur_pos, 9) == 9:
            continue
        # otherwise, add this position to the basin
        basin.add(cur_pos)
        # add neighbors
        for n in neighbors(*cur_pos) & unvisited:
            if n not in q:
                q.append(n)
    return basin


def main():
    fh = sys.stdin
    heightmap = get_heightmap(fh)

    basins = []
    unvisited = {k for k,v in heightmap.items() if v != 9}
    while len(unvisited) > 0:
        start = next(iter(unvisited))
        basins.append(scan_basin(heightmap, start, unvisited))
    print(reduce(int.__mul__, sorted(map(len, basins), reverse=True)[:3]))


main()

