# https://adventofcode.com/2023/day/5


def parse(lines):
    seeds = [int(s) for s in lines[0].split(":")[1].split()]

    maps = []
    current_map = []
    for line in lines[2:]:
        if line.strip() == "":
            maps.append(sorted(current_map))
            current_map = []
            continue

        if line.endswith("map:"):
            continue

        dest, src, length = [int(n) for n in line.split()]
        current_map.append((src, length, dest))

    maps.append(sorted(current_map))

    return seeds, maps


def q1(input):
    seeds, maps = parse(input)
    destinations = []
    for src in seeds:
        # print(f"seed {src}")
        for map in maps:
            for i, (src_range_start, length, dest_range_start) in enumerate(map):
                src_range_end = src_range_start + length
                if src >= src_range_start and src <= src_range_end:
                    if i + 1 < len(map) and src >= map[i + 1][0]:
                        continue
                    src = dest_range_start + (src - src_range_start)
                    break
            # print(f"result={src}")
        destinations.append(src)
    return min(destinations)


# def q2_reverse_mapping(input):
#     seeds, transformations = parse(input)
#     seeds = [(seeds[n * 2], seeds[n * 2 + 1]) for n in range(len(seeds) // 2)]

#     # work backwards from each final output to see if it's possible from the input
#     transformations.reverse()

#     possible_min_locations = []
#     for rule_dest, rule_len, rule_src in transformations[0]:
#         if overlap_start := path_to_seed_exists(
#             rule_dest, rule_dest + rule_len, transformations[1:], seeds
#         ):
#             possible_min_locations += overlap_start

#     return min(possible_min_locations)


# def path_to_seed_exists(range_start, range_end, transformations, seeds):
#     for rule_dest, rule_len, rule_src in transformations[0]:
#         if range_start <= rule_src + rule_len and range_end >= rule_src:
#             # this rule contains a mapping to the next transformation (or seed)
#             overlap_start = max(range_start, rule_dest)
#             overlap_end = min(range_end, rule_dest + rule_len)
#             if len(transformations) == 0:
#                 # base case, there are no more transformation layers
#                 for seed_start, seed_len in seeds:
#                     if (
#                         seed_start >= overlap_start
#                         and seed_start + seed_len <= overlap_end
#                     ):
#                         return overlap_start
#                 return False
#             else:
#                 if path_to_seed_exists(
#                     overlap_start, overlap_end, transformations[1:], seeds
#                 ):
#                     return overlap_start
#     return None


# with a lot of credit to https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/5.py
def q2(input):
    seeds, transformations = parse(input)
    seeds = list(zip(seeds[::2], seeds[1::2]))
    candidates = []
    for seed_start, seed_length in seeds:
        active_ranges = [(seed_start, seed_start + seed_length)]
        for transformation in transformations:
            active_ranges = apply_transformation(transformation, active_ranges)
        candidates.append(min(active_ranges)[0])
    return min(candidates)


def apply_transformation(mappings, ranges):
    result_ranges = []
    for rule_start, rule_length, rule_dest in mappings:
        rule_end = rule_start + rule_length
        temp_ranges = []
        while ranges:
            range_start, range_end = ranges.pop()
            before = (range_start, min(range_end, rule_start))
            within = (max(range_start, rule_start), min(range_end, rule_end))
            after = (max(range_start, rule_end), range_end)
            if before[1] > before[0]:
                temp_ranges.append(before)
            if within[1] > within[0]:
                offset = rule_dest - rule_start
                result_ranges.append((within[0] + offset, within[1] + offset))
            if after[1] > after[0]:
                temp_ranges.append(after)
        ranges = temp_ranges
    return result_ranges + ranges
