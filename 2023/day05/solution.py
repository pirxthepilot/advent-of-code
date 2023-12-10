import json
import sys
from typing import Iterator, List


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Map:
    def __init__(self):
        self.maps = []

    def add(self, line: str) -> None:
        dest, src, counter = [int(i) for i in line.strip().split(" ")]
        self.maps.append({
            "dest": dest,
            "src": src,
            "counter": counter,
        })
    
    def get(self, src: int) -> int:
        for m in self.maps:
            if m["src"] <= src <= m["src"] + m["counter"] - 1:
                return m["dest"] + (src - m["src"])
        return src


class Almanac:
    def __init__(self, text: str):
        self.seeds = []
        self.seed_soil = Map()
        self.soil_fert = Map()
        self.fert_water = Map()
        self.water_light = Map()
        self.light_temp = Map()
        self.temp_humid = Map()
        self.humid_loc = Map()

        mode = ""
        for line in text:
            if not line:
                continue

            if ":" in line:
                mode = line.split(":")[0]
                if mode == "seeds":
                    self._parse_seeds(line.split(":")[1])
                continue
            
            if mode == "seed-to-soil map":
                self.seed_soil.add(line)
            elif mode == "soil-to-fertilizer map":
                self.soil_fert.add(line)
            elif mode == "fertilizer-to-water map":
                self.fert_water.add(line)
            elif mode == "water-to-light map":
                self.water_light.add(line)
            elif mode == "light-to-temperature map":
                self.light_temp.add(line)
            elif mode == "temperature-to-humidity map":
                self.temp_humid.add(line)
            elif mode == "humidity-to-location map":
                self.humid_loc.add(line)
        
    def _parse_seeds(self, line: str) -> None:
        for i in line.strip().split(" "):
            self.seeds.append(int(i))
    
    def show(self) -> str:
        output = {}
        for attribute in (
            "seed_soil",
            "soil_fert",
            "fert_water",
            "water_light",
            "light_temp",
            "temp_humid",
            "humid_loc",
        ):
            output[attribute] = getattr(self, attribute).maps
        return json.dumps(output)
    
    def get(self, seed: int) -> int:
        soil = self.seed_soil.get(seed)
        fert = self.soil_fert.get(soil)
        water = self.fert_water.get(fert)
        light = self.water_light.get(water)
        temp = self.light_temp.get(light)
        humid = self.temp_humid.get(temp)
        loc = self.humid_loc.get(humid)
        # print(f"Seed {seed} -> Soil {soil} -> Fert {fert} -> Water {water} -> Light {light}"
        #         f" -> Temp {temp} -> Humid {humid} -> Loc {loc}")
        return loc

    def get_lowest_loc_from_seeds(self, range_mode=False) -> int:
        lowest = None
        if range_mode:
            for i, s in enumerate(self.seeds):
                if i%2 == 0:  # s is base
                    base = s
                else:         # s is count
                    for seed in range(base, base + s):
                        loc = self.get(seed)
                        if (
                            lowest is None or
                            loc < lowest
                        ):
                            lowest = loc
                            print(f"New lowest loc: {loc}")
        else:
            for seed in self.seeds:
                loc = self.get(seed)
                if (
                    lowest is None or
                    loc < lowest
                ):
                    lowest = loc
        return lowest


def s1(almanac: Almanac) -> int:
    # return almanac.show()
    return almanac.get_lowest_loc_from_seeds()


def s2(almanac: Almanac) -> int:
    # return almanac.show()
    return almanac.get_lowest_loc_from_seeds(range_mode=True)


almanac = Almanac(text)
print(s1(almanac))
print(s2(almanac))
