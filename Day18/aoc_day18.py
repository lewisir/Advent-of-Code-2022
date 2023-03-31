"""
--- Advent of Code 2022 ---
--- Day 18: Boiling Boulders ---
https://adventofcode.com/2022/day/18
"""

from time import perf_counter

TEST = False

DAY = "18"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_data(input_data):
    """process each element in the input data and convert to a tuple of integers"""
    output_data = []
    for coordinate in input_data:
        x, y, z = coordinate.split(",")
        new_coord = tuple((int(x), int(y), int(z)))
        output_data.append(new_coord)
    return output_data


def adjacent_points(point_1, point_2):
    """Given two coordinates compare them to see if they are adjacent"""
    x1, y1, z1 = point_1
    x2, y2, z2 = point_2
    x_diff = abs(x1 - x2)
    y_diff = abs(y1 - y2)
    z_diff = abs(z1 - z2)
    diff = x_diff + y_diff + z_diff
    if x_diff == 1 and y_diff == 0 and z_diff == 0:
        return True
    elif x_diff == 0 and y_diff == 1 and z_diff == 0:
        return True
    elif x_diff == 0 and y_diff == 0 and z_diff == 1:
        return True
    else:
        return False


def main():
    """Main program"""
    boulder_data = process_data(get_input_data(FILENAME))

    adjacent_count = 0
    for index1 in range(len(boulder_data)):
        for index2 in range(index1, len(boulder_data)):
            if adjacent_points(boulder_data[index1], boulder_data[index2]):
                adjacent_count += 2

    total_faces = 6 * len(boulder_data)
    exposed_faces = total_faces - adjacent_count
    print(f"Part I - exposed faces = {exposed_faces}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
