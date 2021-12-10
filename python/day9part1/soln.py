import sys


def get_heightmap(fh):
    heightmap = {}
    for row, row_value in enumerate(fh):
        for col, col_value in enumerate(map(int, row_value.strip())):
            heightmap[row,col] = col_value
    width = col + 1
    height = row + 1
    return heightmap, height, width


def get_lowpoint_heights(heightmap, height, width):
    low_point_heights = []
    for row in range(height):
        for col in range(width):
            h = heightmap.get((row,col))
            neighbor_heights = [
                heightmap.get((row+row_offset,col+col_offset), 10)
                for row_offset, col_offset in [(-1,0),(1,0),(0,-1),(0,1)]
            ]
            if all(
                heightmap.get((row,col)) < neighbor_height
                for neighbor_height in neighbor_heights
            ):
                low_point_heights.append(h)
    return low_point_heights


fh = sys.stdin
low_point_heights = get_lowpoint_heights(*get_heightmap(fh))
print(len(low_point_heights) + sum(low_point_heights))

