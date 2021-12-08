from dataclasses import dataclass
import decimal
from itertools import combinations
import math
import sys
from typing import Optional, Set


def is_point_on_line(l, p):
    return l.A * p.x + l.B * p.y + l.C == 0


def random_point(l):
    # Special case: vertical line
    if l.B == 0:
        x = - l.C / l.A
        # y can be any value
        y = 1
    else:
        # Case: non-vertical line
        x = 1
        y = - (l.A + l.C) / l.B
    return Point(x=x,y=y)


def intersect(l1, l2):
    denominator = (-l2.A * l1.B + l1.A * l2.B)
    # If denominator is 0, the lines are parallel.
    if denominator == 0:
        # Test one point to see if the lines are co-linear.
        # If the lines are co-linear, return the intersection of the rects containing each line.
        if is_point_on_line(l1, random_point(l2)):
            return Line(A=l1.A, B=l1.B, C=l1.C, rect=l1.rect & l2.rect)
        return None
    x = (l1.B * l2.C - l1.C * l2.B) / denominator
    y = (l1.C * l2.A - l2.C * l1.A) / denominator
    p = Point(x=x,y=y)
    if p in (l1.rect & l2.rect):
        return Point(x=x,y=y)
    return None



@dataclass
class Point:
    x: decimal.Decimal
    y: decimal.Decimal
    @classmethod
    def from_ints(cls, x, y):
        return cls(x=decimal.Decimal(x), y=decimal.Decimal(y))
    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Rect:
    minX: decimal.Decimal
    minY: decimal.Decimal
    maxX: decimal.Decimal
    maxY: decimal.Decimal

    def __and__(self, other):
        return Rect(
            minX=max(self.minX, other.minX),
            minY=max(self.minY, other.minY),
            maxX=min(self.maxX, other.maxX),
            maxY=min(self.maxY, other.maxY),
        )

    def __contains__(self, point):
        assert isinstance(point, Point)
        return self.minX <= point.x <= self.maxX and self.minY <= point.y <= self.maxY


@dataclass
class Line:
    """
    Ax + By + C = 0
    """
    A: decimal.Decimal
    B: decimal.Decimal
    C: decimal.Decimal
    rect: Rect
    
    @classmethod
    def from_points(cls, p1, p2):
        if p1.x == p2.x and p1.y == p2.y:
            raise Exception("Points must not be the same!")
        A = p1.y - p2.y
        B = p2.x - p1.x
        C = -A * p1.x - B * p1.y
        return cls(A=A,B=B,C=C,rect=Rect(minX=min(p1.x,p2.x),minY=min(p1.y,p2.y),maxX=max(p1.x,p2.x),maxY=max(p1.y,p2.y)))



def march(self):
    points = set()
    # March along the X axis
    if self.B != 0:
        for x in range(math.ceil(self.rect.minX), math.floor(self.rect.maxX) + 1):
            _x = decimal.Decimal(x)
            y = (-self.A * _x - self.C) / self.B
            points.add(Point(x=_x,y=y))
    elif self.A != 0:
        for y in range(math.ceil(self.rect.minY), math.floor(self.rect.maxY) + 1):
            _y = decimal.Decimal(y)
            x = (-self.B * _y - self.C) / self.A
            points.add(Point(x=x,y=_y))
    else:
        raise Exception("Unexpected state")
    return points


def parse(text_line) -> Line:
    text_p1, text_p2 = text_line.split('->')
    p1 = Point.from_ints(*map(lambda s: int(s.strip()), text_p1.split(',')))
    p2 = Point.from_ints(*map(lambda s: int(s.strip()), text_p2.split(',')))
    return Line.from_points(p1, p2)


def horiz_or_parallel(line):
    return line.A == 0 or line.B == 0


def horiz_parallel_or_diag(line):
    return line.A == 0 or line.B == 0 or abs(line.A) == abs(line.B)


def read_lines(fh):
    return [ parse(l) for l in fh ]


def integer_intersections(l1, l2) -> Set[Point]:
    """Return a list of points with integer only coordinates"""
    intersection = intersect(l1, l2)
    if intersection is None:
        return set()
    if isinstance(intersection, Point):
        if intersection.x % 1 == 0 and intersection.y % 1 == 0:
            return {intersection}
        else:
            return set()
    if isinstance(intersection, Line):
        return march(intersection)
    raise Exception("Unexpected State")



def main():
    fh = sys.stdin

    lines = read_lines(fh)

    # Filter out diagonal lines
    lines = [
        line for line in lines
        if horiz_parallel_or_diag(line)
    ]
    intersections = set()
    for l1, l2 in combinations(lines, 2):
        intersections.update(integer_intersections(l1, l2))
    print(len(intersections))

if __name__ == "__main__":
    main()

