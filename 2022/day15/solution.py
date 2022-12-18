import re


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
        sx, sy = sensor
        distance = self.mapping[sensor]
        step = 1
        while find_distance(sensor, (sx + step, row_y)) < distance:
            step += 1
        start_x = sx - step
        return start_x, step * 2

    def get_beacon_location(self, max_coord=4000000):
        # Part 2
        for y in range(max_coord + 1):
            x = 0
            while x <= max_coord + 1:
                for sensor in self.mapping.keys():
                    start_x, length = self.no_beacons_by_sensor(sensor, y)
                    print((x, y), start_x, length)
                    if start_x <= x <= start_x + length:
                        x = start_x + length + 1
                        print(f"New x: {x}")
                        break
                else:
                    return (x, y)
        # Pregenerate x values
        # x_set = set([x for x in range(max_coord + 1)])

        # for y in range(max_coord + 1):
        #     print(y)
        #     no_beacons_in_x = self.no_beacons_in_row(y)
        #     diff = x_set - no_beacons_in_x
        #     if diff:
        #         return (diff.pop(), y)
            # for d in list(diff):
            #     if 0 <= d <= max_coord:
            #         return (d, y)
            # no_beacons_count = len(self.no_beacons_in_row(y))
            # print(f"{y}: {no_beacons_count}")
            # if no_beacons_count <= max_coord:
            #     print("  Beacon must be in this row ({y})!")
            #     for x in range(max_coord + 1):
            #         distress = (x, y)
            #         for sensor, distance in self.mapping.items():
            #             if find_distance(sensor, distress) <= distance:
            #                 break
            #         else:
            #             return distress
            # x = 0
            # while x <= max_coord:
            #     distress = (x, y)
            #     print(distress)
            #     if distress in no_beacons:
            #         # skip this many x
            #         print(f"Skip {len(no_beacons)}")
            #         x += len(no_beacons)
            #     else:
            #         return distress

            # for x in range(max_coord + 1):
            #     distress = (x, y)
            #     for sensor, distance in self.mapping.items():
            #         if find_distance(sensor, distress) <= distance:
            #             break
            #     else:
            #         return distress


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
# print(m.mapping)
# print(m.max_x(4000000))
# print(m.max_y(4000000))
# p2x, p2y = m.get_beacon_location(20)
# p2x, p2y = m.get_beacon_location(4000000)
# print((p2x, p2y))
# answer_2 = (p2x * 4000000) + p2y
# print(answer_2)
