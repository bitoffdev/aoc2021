from collections import Counter, namedtuple
from contextlib import suppress
import sys


Position = namedtuple('Position', ['row', 'col'])

class Board:

    def __init__(self, num_to_pos):
        self.num_to_pos = num_to_pos
        self.row_counts = Counter({k: 0 for k in range(5)})
        self.col_counts = Counter({k: 0 for k in range(5)})

    def mark(self, number):
        """
        Returns:
            True if this mark caused a bingo, otherwise False
        """
        pos = self.num_to_pos.get(number)
        if pos is None:
            return False
        self.row_counts[pos.row] += 1
        self.col_counts[pos.col] += 1
        return self.row_counts[pos.row] == 5 or self.col_counts[pos.col] == 5

    def score(self, drawn):
        """
        Given the list of numbers drawn so far, return the score of this board
        """
        return sum(filter(lambda x: x not in drawn, self.num_to_pos.keys())) * drawn[-1]


def read_input(fh):
    drawings = [int(x) for x in next(fh).strip().split(',')]
    next(fh)
    boards = set()
    with suppress(StopIteration):
        while True:
            num_to_pos = {}
            for row in range(5):
                for col, value in enumerate(map(int, next(fh).strip().split())):
                    num_to_pos[value] = Position(row, col)
            boards.add(Board(num_to_pos))
            next(fh)
    return drawings, boards


def main():
    fh = sys.stdin
    drawings, boards = read_input(fh)

    drawn = []
    for drawing in drawings:
        drawn.append(drawing)
        winning_boards = set()
        for board in boards:
            if board.mark(drawing):
                winning_boards.add(board)

        # Keep playing until the last board wins
        if len(boards) == 1 and len(winning_boards) == 1:
            break
        # Remove all the winning boards from the competition
        boards = boards - winning_boards
        if len(boards) == 0:
            raise Exception("No boards left to consider. Whoops.")
    else:
        raise Exception("Multiple boards left at the end of the game!")

    sore_loser = boards.pop()
    print(sore_loser.score(drawn))


if __name__ == "__main__":
    main()
