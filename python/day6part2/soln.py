from collections import Counter
import sys


def do_epochs(timer2count: Counter, epochs=256):
    for _ in range(epochs):
        timer2count = Counter({
            (timer - 1): count
            for timer, count in timer2count.items()
        })
        timer2count.update({
            6: timer2count[-1],
            8: timer2count[-1],
        })
        del timer2count[-1]
    return timer2count


def main():
    timer2count = Counter()
    fh = sys.stdin
    for timer in map(int,fh.read().strip().split(",")):
        timer2count.update({ timer: 1})

    timer2count = do_epochs(timer2count)

    print(sum(timer2count.values()))

if __name__ == "__main__":
    main()
