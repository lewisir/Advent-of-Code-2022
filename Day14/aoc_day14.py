"""
--- Advent of Code 2022 ---
--- Day 14: Regolith Reservoir -
--
"""
TEST = False

DAY = "14"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class RockScan:
    """Model the rock formation and fill it with sand"""

    def __init__(self, input_rock_lines) -> None:
        """Initialise the rock scan"""
        self.input_rock_lines = input_rock_lines
        self.coord_pair_list = self.process_input_rock_lines()
        self.rock_formation = self.build_rock_formation()
        self.sand_formation = set(())
        self.deepest_rock = self.find_deepest_rock()

    def convert_string_to_tuple(self, input_string):
        """ "Take a sting of the coordinates and return a tuple"""
        coord_string = input_string.split(",")
        x_coord = int(coord_string[0])
        y_coord = int(coord_string[1])
        return (x_coord, y_coord)

    def process_input_rock_lines(self):
        """Process the input data to produce a list of pairs of coordinates"""
        coord_pair_list = []
        for line in self.input_rock_lines:
            coord_list = line.split(" -> ")
            for index, coord in enumerate(coord_list):
                if index == len(coord_list) - 1:
                    break
                else:

                    coord_pair_list.append(
                        [
                            self.convert_string_to_tuple(coord),
                            self.convert_string_to_tuple(coord_list[index + 1]),
                        ]
                    )
        return coord_pair_list

    def build_rock_formation(self):
        """Build a set of the coordonates that have rocks in them"""
        rock_formation = set(())
        for coordinate_pair in self.coord_pair_list:
            rock_formation.update(
                self.interpolate_cooridnate_pairs(
                    coordinate_pair[0], coordinate_pair[1]
                )
            )
        return rock_formation

    def interpolate_cooridnate_pairs(self, coord_1, coord_2):
        """return the set of coordinates between the pair of coordinates given"""
        x_1, y_1 = coord_1
        x_2, y_2 = coord_2
        if x_1 < x_2:
            x_min, x_max = x_1, x_2
        else:
            x_min, x_max = x_2, x_1
        if y_1 < y_2:
            y_min, y_max = y_1, y_2
        else:
            y_min, y_max = y_2, y_1
        coordinates = set(())
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                coordinates.add((x, y))
        return coordinates

    def find_deepest_rock(self):
        max_y_coord = 0
        for coordinate in self.rock_formation:
            x, y = coordinate
            if y > max_y_coord:
                max_y_coord = y
        return max_y_coord

    def drop_sand(self, x_coord):
        """From the x coorindate drop a unit of sand. Return True if the sand stopped and false if it falls forever"""
        y_coord = 0
        while y_coord <= self.deepest_rock:
            current_coordinate = (x_coord, y_coord)
            next_coordinate = (x_coord, y_coord + 1)
            if next_coordinate in self.rock_formation:
                next_coordinate = (x_coord - 1, y_coord + 1)
                if next_coordinate in self.rock_formation:
                    next_coordinate = (x_coord + 1, y_coord + 1)
                    if next_coordinate in self.rock_formation:
                        self.rock_formation.add(current_coordinate)
                        self.sand_formation.add(current_coordinate)
                        return True
                    else:
                        y_coord += 1
                        x_coord += 1
                else:
                    y_coord += 1
                    x_coord -= 1
            else:
                y_coord += 1
        return False

    def drop_sand_II(self, start_x):
        """From the x coorindate drop a unit of sand..."""
        x_coord = start_x
        y_coord = 0
        while y_coord <= self.deepest_rock + 1:
            current_coordinate = (x_coord, y_coord)
            if (start_x, 0) in self.sand_formation:
                return False
            if y_coord > self.deepest_rock:
                self.rock_formation.add(current_coordinate)
                self.sand_formation.add(current_coordinate)
                return True
            next_coordinate = (x_coord, y_coord + 1)
            if next_coordinate in self.rock_formation:
                next_coordinate = (x_coord - 1, y_coord + 1)
                if next_coordinate in self.rock_formation:
                    next_coordinate = (x_coord + 1, y_coord + 1)
                    if next_coordinate in self.rock_formation:
                        self.rock_formation.add(current_coordinate)
                        self.sand_formation.add(current_coordinate)
                        return True
                    else:
                        y_coord += 1
                        x_coord += 1
                else:
                    y_coord += 1
                    x_coord -= 1
            else:
                y_coord += 1
        return False


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)

    my_rock_formation = RockScan(input_data)
    while my_rock_formation.drop_sand(500):
        pass
    print(f"Part I - {len(my_rock_formation.sand_formation)}")

    my_rock_formation_II = RockScan(input_data)
    while my_rock_formation_II.drop_sand_II(500):
        pass
    print(f"Part II - {len(my_rock_formation_II.sand_formation)}")


if __name__ == "__main__":
    main()
