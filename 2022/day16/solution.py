import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from itertools import permutations


@dataclass
class Path:
    valve: str
    opened: set = field(default_factory=set)
    time_left: int = 30
    pressure: int = 0

    def summarize(self):
        return f"pressure: {self.pressure}, opened: {len(self.opened)}, time: {self.time_left}"


class Map:
    def __init__(self, graph, rates):
        self.graph = graph
        self.rates = rates
        self.map = self._get_pair_distances()
        self.high_score_cache = {}

    def _get_pair_distances(self):
        # included_nodes = [n for n in self.graph.keys() if self.rates[n] != 0]
        included_nodes = self.graph.keys()
        distance_map = defaultdict(dict)

        for pair in permutations(included_nodes, 2):
            start, end = pair
            queue = deque([[start]])
            visited = set()

            while queue:
                path = queue.popleft()
                vertex = path[-1]
                if vertex == end:
                    distance_map[start][end] = len(path) - 1
                    break
                elif vertex not in visited:
                    for neighbor in self.graph[vertex]:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)
                        visited.add(vertex)
        
        return distance_map
    
    def get_max_pressure(self, start_node, time_left=30):
        queue = deque([Path(start_node, time_left=time_left)])

        while queue:
            path = queue.popleft()

            # Open valve if applicable
            if (
                path.valve not in path.opened and
                self.rates[path.valve] != 0
            ):
                path.opened.add(path.valve)
                path.time_left -= 1
                # Calculate accumulated released pressure at end of timer
                # print(path.pressure, path.time_left, self.rates[path.valve])
                path.pressure += path.time_left * self.rates[path.valve]

                # Add to cache if pressure is highest
                if frozenset(path.opened) not in self.high_score_cache:
                    self.high_score_cache[frozenset(path.opened)] = path.pressure
                elif self.high_score_cache[frozenset(path.opened)] < path.pressure:
                    self.high_score_cache[frozenset(path.opened)] = path.pressure
                else:  # Opened valves produce lower score than current highest; no need to continue
                    continue
            yield path

            # Find next open valve
            for neighbor, distance in self.map[path.valve].items():
                if (
                    neighbor not in path.opened and
                    self.rates[neighbor] != 0
                ):
                    new_path = Path(neighbor, path.opened.copy(), time_left=path.time_left, pressure=path.pressure)
                    new_path.time_left -= distance
                    queue.append(new_path)


graph = {}
rates = {}

line_re = re.compile(
    r"Valve (?P<valve>[A-Z]{2}) has flow rate=(?P<frate>\d+); tunnels? leads? to valves? (?P<links>[A-Z ,]+)$"
)
# with open("test.txt") as f:
with open("input.txt") as f:
    for line in f.readlines():
        valve, frate, links = line_re.match(line).groups()
        links = links.split(", ")
        graph[valve] = links
        rates[valve] = int(frate)


# Part 1

m = Map(graph, rates)

highest_pressure = 0
for result in m.get_max_pressure("AA"):
    if result.pressure > highest_pressure:
        highest_pressure = result.pressure
        print(result)


# Part 2

m2 = Map(graph, rates)

for result in m2.get_max_pressure("AA", time_left=26):
    # We only need to run this to generate high_score_cache
    pass

highest_pressure = 0
for pair in permutations(m2.high_score_cache.keys(), 2):
    p1, p2 = pair
    if p1.isdisjoint(p2):
        total = m2.high_score_cache[p1] + m2.high_score_cache[p2]
        if total > highest_pressure:
            highest_pressure = total
            print(f"Highest so far is {total}")
