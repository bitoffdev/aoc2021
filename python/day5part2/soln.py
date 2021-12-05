from dataclasses import dataclass
import decimal
from itertools import combinations
import math
import sys
from typing import Optional


# exact_ctx = decimal.Context(traps=[decimal.Inexact])
# with decimal.localcontext(ctx):
#     result = decimal.Decimal('1') / decimal.Decimal('3')

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
            maxY=min(self.maxX, other.maxY),
        )


@dataclass
class Line:
    """
    Ax + By + C = 0
    """
    A: decimal.Decimal
    B: decimal.Decimal
    C: decimal.Decimal
    minX: decimal.Decimal
    minY: decimal.Decimal
    maxX: decimal.Decimal
    maxY: decimal.Decimal
    rect: Rect
    
    @classmethod
    def from_points(cls, p1, p2):
        if p2.x == p1.x:
            A = decimal.Decimal('1')
            B = decimal.Decimal('0')
            C = -A * p1.x
        else:
            m = (p2.y - p1.y) / (p2.x - p1.x)
            A = m
            B = decimal.Decimal('-1')
            C = -A * p1.x -B * p1.y
        return cls(A=A,B=B,C=C,minX=min(p1.x,p2.x),minY=min(p1.y,p2.y),maxX=max(p1.x,p2.x),maxY=max(p1.y,p2.y),rect=Rect(minX=min(p1.x,p2.x),minY=min(p1.y,p2.y),maxX=max(p1.x,p2.x),maxY=max(p1.y,p2.y)))

    def intersect(self, other) -> Optional[Point]:
        """
        Raises:
            Infinite
        """
        # Bail out for parallel lines
        if self.B * other.A == self.A * other.B:
            return []
        
        # March over the lines
        if self.x < other.x:
            p1 = self
            p2 = other
        else:
            p1 = other
            p2 = self
        import math
        for x in range(math.ceil(p1.x), math.floor(p2.x) + 1):
            y = (-self.A * x - self.C) / self.B

        try:
            y = (self.A * other.C - self.C * other.A) / (self.B * other.A - self.A * other.B)
        except decimal.InvalidOperation as exc:
            print(exc)
            print(dir(exc))
            print(exc.args[0])
            print(exc.args[0] == decimal.DivisionUndefined)
            print(exc.args[0] == decimal.DivisionByZero)
            raise Exception("Infinitely many intersections")
        except decimal.DivisionByZero:
            # Zero intersections, ie. parallel lines
            return None
        
        if self.A == 0:
            x = -(other.B * y + self.C) / other.A
        else:
            x = -(self.B * y + self.C) / self.A
            
        # Check if the intersection is within the segment
        if min(p1.x, p2.x) <= x <= max(p1.x, p2.x) and min(p1.y, p2.y) <= y <= max(p1.y, p2.y):
            return Point(x, y)
        else:
            return None


def march(self):
    points = set()
    # March along the X axis
    if self.B != 0:
        for x in range(math.ceil(self.minX), math.floor(self.maxX) + 1):
            y = (-self.A * x - self.C) / self.B
            points.add(Point(x=x,y=y))
    elif self.A != 0:
        for y in range(math.ceil(self.minY), math.floor(self.maxY) + 1):
            x = (-self.B * y - self.C) / self.A
            points.add(Point(x=x,y=y))
    else:
        raise Exception("Unexpected state")
    return points

def parse(text_line) -> Line:
    text_p1, text_p2 = text_line.split('->')
    p1 = Point.from_ints(*map(lambda s: int(s.strip()), text_p1.split(',')))
    p2 = Point.from_ints(*map(lambda s: int(s.strip()), text_p2.split(',')))
    return Line.from_points(p1, p2)



def horiz_parallel_or_diag(line):
    return line.A == 0 or line.B == 0 or abs(line.A) == abs(line.B)


def read_lines(fh):
    return [ parse(l) for l in fh ]


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
        inter = march(l1) & march(l2)
        intersections.update(inter)
    print(len(intersections))

if __name__ == "__main__":
    main()

