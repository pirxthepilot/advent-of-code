import re
from collections import defaultdict


def get_neighbors(point):
    x, y = point
    return [
        (x, y-1),  # up
        (x+1, y),  # right
        (x, y+1),  # down
        (x-1, y),  # left
    ]


def find_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


class Map:
    def __init__(self, input_):
        # Generate Mapping
        # {
        #   sensor_pos (x,y): distance_from_beacon,
        #   ...
        # }
        self.mapping = {}
        for pair in input_:
            sensor, beacon = pair
            self.mapping[sensor] = find_distance(sensor, beacon)
        self.cache = defaultdict(dict)

    def _add_to_cache(self, sensor, row_y, result):
        _, sy = sensor
        start_x, length = result

        count = 0
        if sy - row_y < 0:
            c_row = row_y
            c_start_x = start_x
            c_length = length
            while c_length > 0:
                self.cache[sensor][c_row] = c_start_x, c_length
                count += 1
                c_row += 1
                c_start_x += 1
                c_length -= 2

        else:
            for i in range(0, sy - row_y + 1):
                # Top
                c_row = row_y + i
                c_start_x = start_x - i
                c_length = length + (2*i)
                self.cache[sensor][c_row] = c_start_x, c_length
                count += 1

                # Bottom (mirror image)
                if c_row != sy:
                    c_row = c_row + ((sy - c_row)*2)
                    self.cache[sensor][c_row] = c_start_x, c_length
                    count += 1

        # print(f"Added {count} items to cache for sensor {sensor}!")

    def no_beacons_in_row(self, row_y):
        include = set()
        for sensor, distance in self.mapping.items():
            sx, sy = sensor

            # get lowest and highest points; include if it crosses row_y
            if (sy + distance) >= row_y >= (sy - distance):
                include.add(sx)   # start point
                direction = 1
                while find_distance(sensor, (sx + direction, row_y)) <= distance:
                    include.add(sx + direction)
                    include.add(sx - direction)
                    direction += 1
        return include

    def no_beacons_by_sensor(self, sensor, row_y):
        if sensor in self.cache and self.cache[sensor].get(row_y):
            return self.cache[sensor][row_y]

        sx, _ = sensor
        distance = self.mapping[sensor]
        step = 0
        while find_distance(sensor, (sx + step, row_y)) < distance:
            step += 1
        start_x = sx - step

        if step > 0:
            result = (start_x, (step * 2) + 1)
            self._add_to_cache(sensor, row_y, result)
            return result

    def get_beacon_location(self, max_coord=4000000):
        # Part 2
        for y in range(max_coord + 1):
            # print(y)
            x = 0
            while 0 <= x <= max_coord + 1:
                for sensor in self.mapping.keys():
                    no_beacons = self.no_beacons_by_sensor(sensor, y)
                    if no_beacons is None:
                        continue
                    start_x, length = no_beacons
                    if start_x <= x < start_x + length:
                        x = start_x + length
                        break
                else:
                    return (x, y)


pairs = []
line_re = re.compile(r"Sensor at x=(?P<sx>[-\d]+), y=(?P<sy>[-\d]+): closest beacon is at x=(?P<bx>[-\d]+), y=(?P<by>[-\d]+)")
# with open("test.txt") as f:
with open("input.txt") as f:
    for line in f.readlines():
        extract = line_re.match(line)
        sx, sy, bx, by = extract.groups()
        pairs.append(((int(sx), int(sy)), (int(bx), int(by))))

m = Map(pairs)


# Part 1

# answer_1 = (len(m.no_beacons_in_row(10)) - 1)
answer_1 = (len(m.no_beacons_in_row(2000000)) - 1)
print(answer_1)


# Part 2

# p2x, p2y = m.get_beacon_location(20)
p2x, p2y = m.get_beacon_location(4000000)
print((p2x, p2y))
answer_2 = (p2x * 4000000) + p2y
print(answer_2)
