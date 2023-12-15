# https://adventofcode.com/2023/day/15


def q1(input):
    total = 0
    for step in "".join(input).split(","):
        total += hash(step)
    return total


def hash(label):
    hash = 0
    for c in label:
        hash += ord(c)
        hash = (hash * 17) % 256
    return hash


def q2(input):
    boxes = [[] for i in range(256)]
    for step in "".join(input).split(","):
        if (eq := step.find("=")) != -1:
            label = step[0:eq]
            focal = int(step[eq + 1 :])
            box = hash(label)
            existing = False
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    boxes[box][i] = (label, focal)
                    existing = True
                    break
            if not existing:
                boxes[box].append((label, focal))
        else:
            label = step[0:-1]
            box = hash(label)
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    del boxes[box][i]

    print("".join([f"{i}: {boxes[i]}, " for i in range(256) if len(boxes[i])]))

    total = 0
    for i in range(256):
        for j, lens in enumerate(boxes[i]):
            total += (i + 1) * (j + 1) * lens[1]
    return total
