# https://adventofcode.com/2023/day/19


from abc import ABC, abstractmethod
from math import prod
import operator


def q1(input):
    parts, workflows = parse(input)
    accepted = []

    for part in parts:
        workflow = workflows["in"]
        while workflow:
            for rule in workflow:
                if rule.passes(part):
                    if rule.dest == "R":
                        workflow = None
                        break
                    if rule.dest == "A":
                        accepted.append(part)
                        workflow = None
                        break
                    workflow = workflows[rule.dest]
                    break

    return sum([sum(part.values()) for part in accepted])


def q2(input):
    _, workflows = parse(input)
    # [print(k, v) for k, v in sorted(workflows.items())]
    paths = bfs(
        workflows["in"],
        workflows,
        {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)},
    )
    return sum(
        [
            prod([filter[1] - filter[0] + 1 for filter in path.values()])
            for path in paths
        ]
    )


def bfs(
    workflow, workflows, current_path: dict[str, tuple[int, int]]
) -> list[dict[str, tuple[int, int]]]:
    # print(f"bfs: {workflow} [{current_path}]")
    rule = workflow.pop(0)

    if isinstance(rule, SimpleRule):
        if rule.dest == "A":
            return [current_path]
        if rule.dest == "R":
            return []
        return bfs(workflows[rule.dest], workflows, current_path)

    mn, mx = current_path[rule.property]
    passing_branch_path = dict(current_path)
    failing_branch_path = dict(current_path)
    if rule.opname == ">":
        passing_branch_path[rule.property] = (max(mn, rule.value + 1), mx)
        failing_branch_path[rule.property] = (mn, min(mx, rule.value))
    else:
        passing_branch_path[rule.property] = (mn, min(mx, rule.value - 1))
        failing_branch_path[rule.property] = (max(mn, rule.value), mx)
    paths_to_good = bfs(workflow, workflows, failing_branch_path)
    if rule.dest not in "AR":
        paths_to_good += bfs(workflows[rule.dest], workflows, passing_branch_path)
    elif rule.dest == "A":
        paths_to_good.append(passing_branch_path)
    return paths_to_good


def parse(input):
    parts = []
    workflows = {}
    for line in input:
        if not line:
            continue
        if line[0] == "{":
            parts.append({tok[0]: int(tok[2:]) for tok in line[1:-1].split(",")})
        else:
            rules = []
            name, steps = line[0:-1].split("{")
            for step in steps.split(","):
                if ":" in step:
                    predicate, dest = step.split(":")
                    rules.append(
                        TestingRule(
                            predicate[0],
                            predicate[1],
                            int(predicate[2:]),
                            dest,
                        )
                    )
                else:
                    rules.append(SimpleRule(step))

            workflows[name] = rules

    return parts, workflows


class Rule(ABC):
    def __init__(self, dest) -> None:
        self.dest = dest

    @abstractmethod
    def passes(self, part) -> bool:
        pass


class SimpleRule(Rule):
    def __init__(self, dest) -> None:
        super().__init__(dest)

    def passes(self, _) -> bool:
        return True

    def __repr__(self) -> str:
        return f">> {self.dest}"


class TestingRule(Rule):
    def __init__(
        self,
        property,
        op,
        value,
        dest,
    ) -> None:
        self.property = property
        self.opname = op
        self.op = operator.lt if op == "<" else operator.gt
        self.value = value
        super().__init__(dest)

    def passes(self, part) -> bool:
        return self.op(part[self.property], self.value)

    def __repr__(self) -> str:
        return f"{self.property}{self.opname}{self.value}? > {self.dest}"
