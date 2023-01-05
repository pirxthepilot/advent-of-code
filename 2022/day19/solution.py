import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from math import ceil, floor
from typing import Tuple


try:
    PART = sys.argv[1]
except IndexError:
    print("Specify a part to run")
    exit()


@dataclass
class State:
    # Timer
    timer: int

    # Robots
    r_ore: int = 0
    r_clay: int = 0
    r_obsidian: int = 0
    r_geode: int = 0

    # Inventory
    i_ore: int = 0
    i_clay: int = 0
    i_obsidian: int = 0
    i_geode: int = 0

    def __hash__(self):
        return hash(
            (self.timer,
            self.r_ore, self.r_clay, self.r_obsidian, self.r_geode,
            self.i_ore, self.i_clay, self.i_obsidian, self.i_geode)
        )
    
    def update_items(self, quantities: Tuple[int]):
        self.i_ore, self.i_clay, self.i_obsidian, self.i_geode = quantities


class BuildOrder:
    blueprint_re = re.compile(
        r"Blueprint (?P<blueprint_id>\d+): "
        r"Each ore robot costs (?P<ore_cost>\d+) ore. "
        r"Each clay robot costs (?P<clay_cost>\d+) ore. "
        r"Each obsidian robot costs (?P<obsidian_cost>\d+) ore and (?P<obsidian_cost_clay>\d+) clay. "
        r"Each geode robot costs (?P<geode_cost>\d+) ore and (?P<geode_cost_obsidian>\d+) obsidian."
    )

    def __init__(self, blueprint: str, timer: int):
        data = self.blueprint_re.match(blueprint)

        self.blueprint_id = int(data.group("blueprint_id"))

        # Robot costs
        self.costs = {
            "ore": {
                "ore": int(data.group("ore_cost"))
            },
            "clay": {
                "ore": int(data.group("clay_cost"))
            },
            "obsidian": {
                "ore": int(data.group("obsidian_cost")),
                "clay": int(data.group("obsidian_cost_clay"))
            },
            "geode": {
                "ore": int(data.group("geode_cost")),
                "obsidian": int(data.group("geode_cost_obsidian"))
            }
        }

        # Start timer
        self.timer = timer

        # Initial state
        self.state = State(self.timer, r_ore=1)

        # Cache
        self.geocache = defaultdict(tuple)

    def print_stats(self):
        print(f"Blueprint {self.blueprint_id}:")
        print(f"  Costs: {self.costs}")
        print(f"  State: {self.state}")
    
    def _better_than_cache(self, state: State) -> bool:
        if not self.geocache[state.timer]:
            self.geocache[state.timer] = (
                state.i_geode,
                state.r_ore,
                state.r_clay,
                state.r_obsidian,
                state.r_geode,
            )
            return True

        ci_ge, cr_or, cr_cl, cr_ob, cr_ge = self.geocache[state.timer]
        if (
            cr_or == state.r_ore and
            cr_cl == state.r_clay and
            cr_ob == state.r_obsidian and
            cr_ge == state.r_geode
        ):
            if ci_ge < state.i_geode:
                self.geocache[state.timer] = (
                    state.i_geode,
                    state.r_ore,
                    state.r_clay,
                    state.r_obsidian,
                    state.r_geode,
                )
                return True
            return False
        return True

    def _gen_next_state(self, state: State, turns: int) -> State:
        """ Create the next state based on current state """
        # Updated inventory
        ore = state.i_ore + (state.r_ore * turns)
        clay = state.i_clay + (state.r_clay * turns)
        obsidian = state.i_obsidian + (state.r_obsidian * turns)
        geode = state.i_geode + (state.r_geode * turns)

        return State(
            state.timer - turns,
            r_ore=state.r_ore,
            r_clay=state.r_clay,
            r_obsidian=state.r_obsidian,
            r_geode=state.r_geode,
            i_ore=ore,
            i_clay=clay,
            i_obsidian=obsidian,
            i_geode=geode,
        )
    
    def _next_ore_robot(self, state: State):
        if state.r_obsidian > 0:
            return self._gen_next_state(state, state.timer)
        
        if state.r_geode > 0:
            return None
        
        max_ore_for_next_robot = max([
            # self.costs["ore"]["ore"],
            self.costs["clay"]["ore"],
            self.costs["obsidian"]["ore"],
            self.costs["geode"]["ore"],
        ])
        if state.r_ore >= max_ore_for_next_robot:
            return None

        cost = self.costs["ore"]["ore"]
        turns = ceil((cost - state.i_ore) / state.r_ore)
        turns = 0 if turns < 0 else turns

        if state.timer <= turns + 1:
            return None

        harvest_state = self._gen_next_state(state, turns)
        qty = floor(harvest_state.i_ore / cost)
        build_state = self._gen_next_state(harvest_state, 1)
        build_state.i_ore -= cost * qty
        build_state.r_ore += qty 

        return build_state

    def _next_clay_robot(self, state: State):
        if state.r_geode > 0:
            return None

        max_ore_for_next_robot = max([
            self.costs["obsidian"]["clay"],
        ])
        if state.r_clay >= max_ore_for_next_robot:
            return None

        cost = self.costs["clay"]["ore"]
        turns = ceil((cost - state.i_ore) / state.r_ore)
        turns = 0 if turns < 0 else turns

        if state.timer <= turns + 1:
            return None

        harvest_state = self._gen_next_state(state, turns)
        qty = floor(harvest_state.i_ore / cost)
        build_state = self._gen_next_state(harvest_state, 1)
        build_state.i_ore -= cost * qty
        build_state.r_clay += qty 

        return build_state

    def _next_obsidian_robot(self, state: State):
        if state.r_clay == 0:
            return None

        if state.r_geode >= 2 and state.r_obsidian >= state.r_geode:
            return None

        max_ore_for_next_robot = max([
            self.costs["geode"]["obsidian"],
        ])
        if state.r_obsidian >= max_ore_for_next_robot:
            return None

        cost_o = self.costs["obsidian"]["ore"]
        cost_c = self.costs["obsidian"]["clay"]

        turns = max([
            ceil((cost_o - state.i_ore) / state.r_ore),
            ceil((cost_c - state.i_clay) / state.r_clay),
        ])
        turns = 0 if turns < 0 else turns

        if state.timer <= turns + 1:
            return None

        harvest_state = self._gen_next_state(state, turns)
        qty = min([
            floor(harvest_state.i_ore / cost_o),
            floor(harvest_state.i_clay / cost_c),
        ])
        build_state = self._gen_next_state(harvest_state, 1)
        build_state.i_ore -= cost_o * qty
        build_state.i_clay -= cost_c * qty
        build_state.r_obsidian += qty 

        return build_state

    def _next_geode_robot(self, state: State):
        if (
            state.r_clay == 0 or
            state.r_obsidian == 0
        ):
            return None
        
        cost_o = self.costs["geode"]["ore"]
        cost_b = self.costs["geode"]["obsidian"]

        turns = max([
            ceil((cost_o - state.i_ore) / state.r_ore),
            ceil((cost_b - state.i_obsidian) / state.r_obsidian),
        ])
        turns = 0 if turns < 0 else turns

        if state.timer <= turns + 1:
            return None

        harvest_state = self._gen_next_state(state, turns)
        qty = min([
            floor(harvest_state.i_ore / cost_o),
            floor(harvest_state.i_obsidian / cost_b),
        ])
        build_state = self._gen_next_state(harvest_state, 1)
        build_state.i_ore -= cost_o * qty
        build_state.i_obsidian -= cost_b * qty
        build_state.r_geode += qty 

        return build_state

    def run(self):
        print("\n== START SIMULATION ==\n")
        self.print_stats()
        print()

        queue = deque([self.state])
        visited = set() 

        while queue:
            state = queue.popleft()

            if state.timer == 0:
                yield state
            elif state not in visited:
                # Last few turns - do not branch anymore
                if state.timer == 1:
                    queue.append(self._gen_next_state(state, state.timer))
                    continue
                
                # Potential to max - discard if none
                if not self._better_than_cache(state):
                    continue

                # Possible next states
                for next_state in [
                    self._next_ore_robot(state),
                    self._next_clay_robot(state),
                    self._next_obsidian_robot(state),
                    self._next_geode_robot(state),
                ]:
                    if next_state is not None:
                        queue.append(next_state)


# with open("test.txt") as f:
with open("input.txt") as f:
    blueprints = [l.strip() for l in f.readlines()]


## Part 1

if int(PART) == 1:
    quality_levels = []
    for blueprint in blueprints:
        bp = BuildOrder(blueprint, 24)
        max_geode = 0
        for state in bp.run():
            if state.i_geode > max_geode:
                print(f"  New highest geode: {state}")
                max_geode = state.i_geode
        quality_levels.append(bp.blueprint_id * max_geode) 
        print(f"Q: {quality_levels}")

    print(quality_levels)
    answer_1 = sum(quality_levels)
    print(answer_1)


## Part 2

elif int(PART) == 2:
    geode_product = 1
    # for blueprint in blueprints[1:2]:
    for blueprint in blueprints[:3]:
        bp = BuildOrder(blueprint, 32)
        max_geode = 0
        for state in bp.run():
            if state.i_geode > max_geode:
                print(f"  New highest geode: {state}")
                max_geode = state.i_geode
        geode_product *= max_geode

    answer_2 = geode_product
    print(answer_2)
