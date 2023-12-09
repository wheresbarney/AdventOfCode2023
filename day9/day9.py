# https://adventofcode.com/2023/day/9


from functools import reduce


def q1(input):
    histories = [[int(n) for n in line.split()] for line in input]
    ret = 0
    for history in histories:
        terminals = [history[-1]]
        while any([h != history[0] for h in history[1:]]):
            history = [history[i] - history[i - 1] for i in range(1, len(history))]
            terminals.append(history[-1])
        ret += sum(terminals)
    return ret


def q2(input):
    histories = [[int(n) for n in line.split()] for line in input]
    ret = 0
    for history in histories:
        lterminals = [history[0]]
        while any([h != history[0] for h in history[1:]]):
            history = [history[i] - history[i - 1] for i in range(1, len(history))]
            lterminals.append(history[0])
        ret += reduce(lambda acc, lterm: lterm - acc, reversed(lterminals))
    return ret
