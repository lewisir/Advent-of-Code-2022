"""
--- Advent of Code 2022 ---
--- Day 15: Beacon Exclusion Zone ---
https://adventofcode.com/2022/day/15
"""
TEST = False

DAY = "15"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
    LIMIT = 20
else:
    FILENAME = REAL_INPUT
    LIMIT = 4000000


from cmath import inf


class BeaconZone:
    """Model the Zone that is popualted by scanners that detect beacons"""

    def __init__(self, input_data) -> None:
        self.input_data = input_data
        self.sensor_list = []
        self.beacon_list = []
        self.sensor_exclusion_distances = {}
        self.populate_data()
        self.beacon_exclusion_set = set(())

    def populate_data(self):
        """Extract each sensor from the input data and add to the sensor_list"""
        for data in self.input_data:
            sensor = data[0]
            sensor_x, sensor_y = sensor
            beacon = data[1]
            beacon_x, beacon_y = beacon
            distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            self.sensor_list.append(sensor)
            self.beacon_list.append(beacon)
            self.sensor_exclusion_distances[sensor] = distance

    def exclusion_zone(self, sensor, distance):
        """return the set of points within the distance of the sensor"""
        coord_set = set(())
        sensor_x, sensor_y = sensor
        for d in range(distance + 1):
            for x in range(d + 1):
                for x_coord in range(sensor_x - x, sensor_x + x + 1):
                    for y_coord in range(sensor_y - (d - x), sensor_y + (d - x) + 1):
                        coord_set.add((x_coord, y_coord))
        return coord_set

    def exclusion_row(self, sensor, distance, row, limit=float(inf)):
        """return the set of points on the row within the distance to the sensor limited to the x limit"""
        coord_set = set(())
        sensor_x, sensor_y = sensor
        x_allowance = distance - abs(sensor_y - row)
        for x_coord in range(sensor_x - x_allowance, sensor_x + x_allowance + 1):
            if x_coord <= limit and x_coord >= 0:
                coord_set.add((x_coord, row))
        return coord_set

    def populate_beacon_exclusion(self):
        """update the beacon_exclusion_set with all the point that cannot have a beacon in them"""
        for sensor, distance in self.sensor_exclusion_distances.items():
            self.beacon_exclusion_set.update(self.exclusion_zone(sensor, distance))
        for beacon in self.beacon_list:
            self.beacon_exclusion_set.discard(beacon)

    def count_exclusion_points(self, row):
        """Provide the Y coordinate and count the number of points in the row that cannot have a beacon"""
        point_count = 0
        for coord in self.beacon_exclusion_set:
            x_coord, y_coord = coord
            if y_coord == row:
                point_count += 1
        return point_count

    def empty_points(self, row):
        """A new method to count points in a row that cannot hold a beacon"""
        coord_set = set(())
        for sensor, distance in self.sensor_exclusion_distances.items():
            sensor_x, sensor_y = sensor
            if abs(sensor_y - row) <= distance:
                coord_set.update(self.exclusion_row(sensor, distance, row))
        for beacon in self.beacon_list:
            coord_set.discard(beacon)
        return len(coord_set)

    def limited_empty_points(self, row, limit):
        """count the points in the row that cannot hold a beacon up to the limit in x"""
        coord_set = set(())
        for sensor, distance in self.sensor_exclusion_distances.items():
            sensor_x, sensor_y = sensor
            if abs(sensor_y - row) <= distance:
                coord_set.update(self.exclusion_row(sensor, distance, row, limit))
        return len(coord_set)

    def non_empty_points(self, row, limit):
        """Return a set of points that could contain beacson given the row and limit"""
        coord_set = set(())
        for x_coord in range(limit + 1):
            coord_set.add((x_coord, row))
        for sensor, distance in self.sensor_exclusion_distances.items():
            sensor_x, sensor_y = sensor
            if abs(sensor_y - row) <= distance:
                for coord in self.inclusion_row(sensor, distance, row, limit):
                    coord_set.discard(coord)
        return coord_set

    def inclusion_row(self, sensor, distance, row, limit=float(inf)):
        """return the set of points on the row greater than the distance to the sensor limited to the x limit"""
        coord_set = set(())
        sensor_x, sensor_y = sensor
        x_allowance = distance - abs(sensor_y - row)
        for x_coord in range(sensor_x - x_allowance, sensor_x + x_allowance + 1):
            if x_coord <= limit and x_coord >= 0:
                coord_set.add((x_coord, row))
        return coord_set


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_input_data(input_data):
    """process the input data to extract each scanner and its closest Beacon"""
    sensor_list = []
    for line in input_data:
        sensor_data = line.split(":")[0]
        beacon_data = line.split(":")[1]
        sensor_x = int(
            sensor_data[sensor_data.find("x=") + 2 : sensor_data.find(", y=")]
        )
        sensor_y = int(sensor_data[sensor_data.find("y=") + 2 :])
        sensor_coord = (sensor_x, sensor_y)
        beacon_x = int(
            beacon_data[beacon_data.find("x=") + 2 : beacon_data.find(", y=")]
        )
        beacon_y = int(beacon_data[beacon_data.find("y=") + 2 :])
        beacon_coord = (beacon_x, beacon_y)
        sensor_list.append([sensor_coord, beacon_coord])
    return sensor_list


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    data = process_input_data(input_data)
    my_zone = BeaconZone(data)
    print(
        f"Part I - Row 10 contains {my_zone.empty_points(10)} points that cannot contain a beacon"
    )

    for row in range(LIMIT + 1):
        if my_zone.limited_empty_points(row, LIMIT) < LIMIT + 1:
            beacon_row = row
    beacon_set = my_zone.non_empty_points(beacon_row, LIMIT)
    if len(beacon_set) == 1:
        for beacon_coord in beacon_set:
            beacon_x, beacon_y = beacon_coord
        tuning_frequency = beacon_x * 4000000 + beacon_y
        print(f"Part II - Tuning Frequency {tuning_frequency}")


if __name__ == "__main__":
    main()
