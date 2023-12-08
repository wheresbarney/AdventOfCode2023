# https://adventofcode.com/2023/day/8


from math import lcm


def parse(input):
    directions = input[0]
    lines = [
        line.replace("=", "").replace("(", "").replace(")", "").replace(",", "").split()
        for line in input[2:]
    ]
    nodes = {line[0]: (line[1], line[2]) for line in lines}
    return directions, nodes


def q1(input):
    directions, nodes = parse(input)
    steps = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        direction = directions[steps % len(directions)]
        dirkey = 0 if direction == "L" else 1
        current_node = nodes[current_node][dirkey]
        steps += 1
    return steps


# def q2_brute_force(input):
#     directions, nodes = parse(input)
#     current_nodes = [node for node in nodes.keys() if node.endswith("A")]
#     steps = 0
#     while any([not node.endswith("Z") for node in current_nodes]):
#         # print(f"{steps}: {current_nodes}")
#         direction = directions[steps % len(directions)]
#         dirkey = 0 if direction == "L" else 1
#         current_nodes = [nodes[n][dirkey] for n in current_nodes]
#         # print(f"  --> {current_nodes}")
#         steps += 1
#     return steps


def q2(input):
    directions, nodes = parse(input)

    def solve(n):
        steps = 0
        while not n.endswith("Z"):
            direction = directions[steps % len(directions)]
            dirkey = 0 if direction == "L" else 1
            n = nodes[n][dirkey]
            steps += 1
        return steps

    first_zeds = [solve(node) for node in nodes.keys() if node.endswith("A")]
    return lcm(*first_zeds)


# def cycle_time(original_node, directions, nodes):
#     node = original_node
#     steps = 0
#     visited = {}
#     terms = set()
#     while True:
#         visit_key = (node, steps % len(directions))
#         if visit_key in visited:
#             print(
#                 f"cycle detected for {original_node} "
#                 + f"at {visited[visit_key]}->{steps} {terms}"
#             )
#             # assume there is only ever one terminal in each path
#             return steps_to_next_z(original_node, visit_key[1], steps, terms.pop())
#         visited[visit_key] = steps

#         if node.endswith("Z"):
#             terms.add(steps)

#         direction = directions[steps % len(directions)]
#         dirkey = 0 if direction == "L" else 1
#         node = nodes[node][dirkey]
#         steps += 1


# def steps_to_next_z(label, lead, step, z):
#     while True:
#         # print(f"  {label}: {z} (and moving to {z + step - lead})")
#         yield z
#         z += step - lead


# def q2(input):
#     directions, nodes = parse(input)
#     paths = [
#         cycle_time(node, directions, nodes)
#         for node in nodes.keys()
#         if node.endswith("A")
#     ]
#     zeds = [next(path) for path in paths]
#     while True:
#         if all(z == zeds[0] for z in zeds[1:]):
#             return zeds[0]

#         for i in range(len(paths) - 1):
#             if zeds[i] < zeds[i + 1]:
#                 zeds[i] = next(paths[i])
#             elif zeds[i] > zeds[i + 1]:
#                 zeds[i + 1] = next(paths[i + 1])
