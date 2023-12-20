# https://adventofcode.com/2023/day/20


from abc import ABC, abstractmethod
from math import prod, lcm


class Module(ABC):
    def __init__(self, name: str, sends_to: list[str]) -> None:
        self.name = name
        self.sends_to = sends_to

    @abstractmethod
    def process_pulse(self, hi: bool, sender: str) -> list[tuple[str, bool, str]]:
        pass


def q1(input):
    nodes = parse(input)
    event_counts = {True: 0, False: 0}
    for _ in range(1000):
        events = [("broadcaster", False, "button")]
        while events:
            to, hi, sender = events.pop(0)
            event_counts[hi] += 1
            if to not in nodes:
                continue
            events += nodes[to].process_pulse(hi, sender)
        # print(nodes)

    return prod(event_counts.values())


# https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0A%0A%20%20cf%20-%3E%20hl%2C%20qt_AND%3B%0A%20%20bn_AND%20-%3E%20rx%3B%0A%20%20nb%20-%3E%20vt_AND%3B%0A%20%20hm%20-%3E%20jp%3B%0A%20%20vr%20-%3E%20qt_AND%2C%20sl%3B%0A%20%20gq%20-%3E%20hm%2C%20nl_AND%3B%0A%20%20sl%20-%3E%20jx%2C%20qt_AND%3B%0A%20%20pl_AND%20-%3E%20bn_AND%3B%0A%20%20hf%20-%3E%20vt_AND%2C%20ch%3B%0A%20%20kx%20-%3E%20dq_AND%3B%0A%20%20fr%20-%3E%20qf%3B%0A%20%20rh%20-%3E%20vr%3B%0A%20%20vt_AND%20-%3E%20lz_AND%2C%20dh%2C%20kr%2C%20kq%2C%20lm%2C%20qk%3B%0A%20%20dq_AND%20-%3E%20mz_AND%2C%20ml%2C%20xd%2C%20fb%2C%20xs%2C%20rc%2C%20rt%3B%0A%20%20hn%20-%3E%20qk%2C%20vt_AND%3B%0A%20%20bv%20-%3E%20nl_AND%3B%0A%20%20jv%20-%3E%20rh%2C%20qt_AND%3B%0A%20%20kq%20-%3E%20lm%3B%0A%20%20nd%20-%3E%20hp%3B%0A%20%20gj%20-%3E%20bv%2C%20nl_AND%3B%0A%20%20lv%20-%3E%20xs%2C%20dq_AND%3B%0A%20%20ch%20-%3E%20vt_AND%2C%20kd%3B%0A%20%20sm%20-%3E%20qt_AND%2C%20nd%3B%0A%20%20nt%20-%3E%20jv%3B%0A%20%20qk%20-%3E%20cb%3B%0A%20%20jx%20-%3E%20cf%3B%0A%20%20hl%20-%3E%20qt_AND%2C%20ng%3B%0A%20%20qt_AND%20-%3E%20sm%2C%20rh%2C%20nd%2C%20jx%2C%20nt%2C%20pl_AND%3B%0A%20%20bh%20-%3E%20nl_AND%2C%20fr%3B%0A%20%20kd%20-%3E%20vt_AND%2C%20nb%3B%0A%20%20gx%20-%3E%20mh%2C%20dq_AND%3B%0A%20%20hp%20-%3E%20nt%2C%20qt_AND%3B%0A%20%20rc%20-%3E%20lv%3B%0A%20%20broadcaster%20-%3E%20kr%2C%20zb%2C%20sm%2C%20xd%3B%0A%20%20mz_AND%20-%3E%20bn_AND%3B%0A%20%20qf%20-%3E%20rd%2C%20nl_AND%3B%0A%20%20sk%20-%3E%20nl_AND%2C%20bh%3B%0A%20%20rb%20-%3E%20nl_AND%2C%20sk%3B%0A%20%20cb%20-%3E%20hf%2C%20vt_AND%3B%0A%20%20fb%20-%3E%20rt%3B%0A%20%20lz_AND%20-%3E%20bn_AND%3B%0A%20%20mh%20-%3E%20dq_AND%2C%20kx%3B%0A%20%20rt%20-%3E%20mt%3B%0A%20%20xd%20-%3E%20dq_AND%2C%20fb%3B%0A%20%20lm%20-%3E%20hn%3B%0A%20%20hh%20-%3E%20vt_AND%2C%20dh%3B%0A%20%20ml%20-%3E%20ts%3B%0A%20%20mt%20-%3E%20rc%2C%20dq_AND%3B%0A%20%20ts%20-%3E%20gx%2C%20dq_AND%3B%0A%20%20rd%20-%3E%20nl_AND%2C%20gq%3B%0A%20%20zb%20-%3E%20nl_AND%2C%20rb%3B%0A%20%20kr%20-%3E%20hh%2C%20vt_AND%3B%0A%20%20nl_AND%20-%3E%20fr%2C%20zb%2C%20hm%2C%20zm_AND%3B%0A%20%20zm_AND%20-%3E%20bn_AND%3B%0A%20%20dh%20-%3E%20kq%3B%0A%20%20ng%20-%3E%20qt_AND%3B%0A%20%20xs%20-%3E%20ml%3B%0A%20%20jp%20-%3E%20nl_AND%2C%20gj%3B%0A%20%20broadcaster%20%5Bshape%3DMdiamond%5D%3B%0A%20%20rx%20%5Bshape%3DMsquare%5D%3B%0A%7D
def q2(input):
    nodes = parse(input)
    pushes = 0
    lcms = {}
    while True:
        pushes += 1
        events = [("broadcaster", False, "button")]
        while events:
            to, hi, sender = events.pop(0)
            if to == "rx" and not hi:
                return pushes
            if hi and sender in ["pl", "lz", "zm", "mz"]:
                print(f"{'hi' if hi else 'lo'} from {sender} after {pushes} pushes")
                lcms[sender] = pushes
                if len(lcms) == 4:
                    return lcm(*lcms.values())
            if to not in nodes:
                continue
            events += nodes[to].process_pulse(hi, sender)


def parse(input) -> dict[str, Module]:
    graph = {}
    for line in input:
        name, sends_to = line.split(" -> ")
        sends_to = sends_to.split(", ")
        if name[0] == "%":
            graph[name[1:]] = FlipFlopModule(name[1:], sends_to)
        elif name[0] == "&":
            graph[name[1:]] = ConjunctionModule(name[1:], sends_to)
        else:
            graph[name] = BroadcastModule(name, sends_to)

    for name, module in graph.items():
        for sends_to in module.sends_to:
            if sends_to not in graph:
                continue
            if isinstance(graph[sends_to], ConjunctionModule):
                graph[sends_to].register_upstream(name)

    return graph


class BroadcastModule(Module):
    def __init__(self, name: str, sends_to: list[str]) -> None:
        super().__init__(name, sends_to)

    def __repr__(self) -> str:
        return f"{self.name}[Broadcast]"

    def process_pulse(self, hi: bool, _: str) -> list[tuple[str, bool, str]]:
        return [(to, hi, self.name) for to in self.sends_to]


class FlipFlopModule(Module):
    def __init__(self, name: str, sends_to: list[str]) -> None:
        super().__init__(name, sends_to)
        self.state = False

    def __repr__(self) -> str:
        return f"{self.name}[FlipFlop] active={self.state}"

    def process_pulse(self, hi: bool, sender: str) -> list[tuple[str, bool, str]]:
        if hi:
            return []
        self.state = not self.state
        return [(to, self.state, self.name) for to in self.sends_to]


class ConjunctionModule(Module):
    def __init__(self, name: str, sends_to: list[str]) -> None:
        super().__init__(name, sends_to)
        self.state = {}

    def __repr__(self) -> str:
        return f"{self.name}[Conjunction] {self.state}"

    def register_upstream(self, upstream: str) -> None:
        self.state[upstream] = False

    def process_pulse(self, hi: bool, sender: str) -> list[tuple[str, bool, str]]:
        self.state[sender] = hi
        return [
            (to, any([not v for v in self.state.values()]), self.name)
            for to in self.sends_to
        ]
