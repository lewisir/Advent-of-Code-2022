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
    ROW = 10
else:
    FILENAME = REAL_INPUT
    LIMIT = 4000000
    ROW = 2000000


from time import perf_counter


class BeaconZone:
    """Model the Zone that is popualted by scanners that detect beacons"""

    def __init__(self, input_data) -> None:
        self.input_data = input_data
        self.sensor_list = set(())
        self.beacon_list = set(())
        self.sensor_exclusion_distances = {}
        self.populate_data()

    def populate_data(self) -> None:
        """Extract each sensor from the input data and
        update the sensor, beacon and exclusion distance lists"""
        for data in self.input_data:
            sensor = data[0]
            sensor_x, sensor_y = sensor
            beacon = data[1]
            beacon_x, beacon_y = beacon
            distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            self.sensor_list.add(sensor)
            self.beacon_list.add(beacon)
            self.sensor_exclusion_distances[sensor] = distance

    def sensor_exclusion_range(self, sensor, coord, ordinate="row"):
        """Given a row or column and sensor, return the range of values in the row/column that the sensor covers"""
        sensor_x, sensor_y = sensor
        distance = self.sensor_exclusion_distances[sensor]
        if ordinate == "row":
            # y_diff = abs(sensor_y - coord)
            diff = abs(sensor_y - coord)
        elif ordinate == "col":
            diff = abs(sensor_x - coord)
        else:
            print("Bad Ordinate")

        if diff <= distance:
            coordinate_range = distance - diff
            if ordinate == "row":
                coordinate_min = sensor_x - coordinate_range
                coordinate_max = sensor_x + coordinate_range
            elif ordinate == "col":
                coordinate_min = sensor_y - coordinate_range
                coordinate_max = sensor_y + coordinate_range
            return (coordinate_min, coordinate_max)
        else:
            return None

    def exclusion_ranges(self, coorindate, ordinate="row"):
        exc_ranges = []
        for sensor in self.sensor_exclusion_distances:
            sen_exc_range = self.sensor_exclusion_range(sensor, coorindate, ordinate)
            if sen_exc_range is not None:
                exc_ranges.append(sen_exc_range)
        exc_ranges.sort()
        collapsed_ranges = self.collapse_ranges(exc_ranges)
        return collapsed_ranges

    def collapse_ranges(self, range_list):
        """Given a list of tuples which are ranges, collapse the ranges to a smaller set"""
        new_ranges = []
        new_min, new_max = None, None
        for sub_range in range_list:
            current_min, current_max = sub_range
            if new_min is None:
                new_min = current_min
            if new_max is None:
                new_max = current_max

            if current_min > new_max + 1:
                new_ranges.append((new_min, new_max))
                new_min, new_max = current_min, current_max
            elif current_max > new_max:
                new_max = current_max
        if new_min is None:
            new_min = current_min
        if new_max is None:
            new_max = current_max
        new_ranges.append((new_min, new_max))
        return new_ranges

    def count_in_ranges(
        self, range_list, lower_limit=float("-inf"), upper_limit=float("inf")
    ):
        """count the number of points covered by a list of ranges"""
        count = 0
        for range_space in range_list:
            current_min, current_max = range_space
            if current_min <= lower_limit:
                use_min = lower_limit
            else:
                use_min = current_min
            if current_max >= upper_limit:
                use_max = upper_limit
            else:
                use_max = current_max
            count += use_max - use_min + 1
        return count

    def value_in_ranges(self, range_list, value):
        """Return true of the value is within the range list"""
        for range_space in range_list:
            current_min, current_max = range_space
            if value <= current_max and value >= current_min:
                return True
        return False

    def gaps_in_range(self, range_list):
        """Given  range list return the value that is missing from the range list"""
        return range_list[0][1] + 1


def get_input_data(filename) -> list:
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_input_data(input_data) -> list:
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
    exclusion_count = my_zone.count_in_ranges(my_zone.exclusion_ranges(ROW))

    for beacon in my_zone.beacon_list:
        if (
            my_zone.value_in_ranges(my_zone.exclusion_ranges(ROW), beacon[0])
            and beacon[1] == ROW
        ):
            exclusion_count -= 1
    print(f"Part I - {exclusion_count}")

    for y in range(LIMIT + 1):
        exclusion_range = my_zone.exclusion_ranges(y, "row")
        exclusion_count = my_zone.count_in_ranges(exclusion_range, 0, LIMIT)
        if exclusion_count < LIMIT + 1:
            row = y
            col = my_zone.gaps_in_range(exclusion_range)
            break
    print(f"x {col} and y {row} and answer is {4000000*col + row}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
