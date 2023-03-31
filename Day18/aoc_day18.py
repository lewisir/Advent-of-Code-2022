"""
--- Advent of Code 2022 ---
--- Day 18: Boiling Boulders ---
https://adventofcode.com/2022/day/18
"""

from time import perf_counter
import sys

sys.setrecursionlimit(9999999)
TEST = False

DAY = "18"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class LavaBoulder:
    """Model the lava boulder"""

    def __init__(self, boulder_data):
        self.boulder_data = boulder_data
        self.total_surface_area = self.surface_area(self.boulder_data)
        self.min_x, self.min_y, self.min_z = self.boulder_limits()[0]
        self.max_x, self.max_y, self.max_z = self.boulder_limits()[1]
        self.total_box = self.create_total_box()
        self.negative_data = self.total_box.difference(set(boulder_data))
        self.vaccum_packed_boulder = self.total_box.difference(
            self.search_surrounding_space(
                (self.min_x - 1, self.min_y - 1, self.min_z - 1), set(())
            )
        )
        self.total_external_area = self.surface_area(list(self.vaccum_packed_boulder))

    def adjacent_points(self, point_1, point_2):
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

    def surface_area(self, input_data):
        """calcualte the total surface area of the boulder"""
        adjacent_count = 0
        for index1 in range(len(input_data)):
            for index2 in range(index1, len(input_data)):
                if self.adjacent_points(input_data[index1], input_data[index2]):
                    adjacent_count += 2

        total_faces = 6 * len(input_data)
        return total_faces - adjacent_count

    def boulder_limits(self):
        """find the minimum and maximum points of a box that encloses the boulder"""
        min_x, max_x, min_y, max_y, min_z, max_z = (
            float("inf"),
            0,
            float("inf"),
            0,
            float("inf"),
            0,
        )
        for point in self.boulder_data:
            x, y, z = point
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
            if z < min_z:
                min_z = z
            if z > max_z:
                max_z = z
        return [(min_x, min_y, min_z), (max_x, max_y, max_z)]

    def create_total_box(self):
        """create a set of all points given the boulder's limits"""
        total_set = set(())
        for x in range(self.min_x - 1, self.max_x + 2):
            for y in range(self.min_y - 1, self.max_y + 2):
                for z in range(self.min_z - 1, self.max_z + 2):
                    total_set.add((x, y, z))
        return total_set

    def search_surrounding_space(self, point, surrounding_points):
        """identify all the points outside of the boulder within the eclosing box"""
        surrounding_points.add(point)
        x, y, z = point
        if (x + 1, y, z) not in surrounding_points and (
            x + 1,
            y,
            z,
        ) in self.negative_data:
            self.search_surrounding_space((x + 1, y, z), surrounding_points)
        if (x - 1, y, z) not in surrounding_points and (
            x - 1,
            y,
            z,
        ) in self.negative_data:
            self.search_surrounding_space((x - 1, y, z), surrounding_points)
        if (x, y + 1, z) not in surrounding_points and (
            x,
            y + 1,
            z,
        ) in self.negative_data:
            self.search_surrounding_space((x, y + 1, z), surrounding_points)
        if (x, y - 1, z) not in surrounding_points and (
            x,
            y - 1,
            z,
        ) in self.negative_data:
            self.search_surrounding_space((x, y - 1, z), surrounding_points)
        if (x, y, z + 1) not in surrounding_points and (
            x,
            y,
            z + 1,
        ) in self.negative_data:
            self.search_surrounding_space((x, y, z + 1), surrounding_points)
        if (x, y, z - 1) not in surrounding_points and (
            x,
            y,
            z - 1,
        ) in self.negative_data:
            self.search_surrounding_space((x, y, z - 1), surrounding_points)
        return surrounding_points


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


def main():
    """Main program"""
    boulder_data = process_data(get_input_data(FILENAME))
    my_boulder = LavaBoulder(boulder_data)
    print(f"Part I surface area is {my_boulder.total_surface_area}")
    print(f"Part II external surface area is {my_boulder.total_external_area}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
