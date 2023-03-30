"""
--- Advent of Code 2022 ---
--- Day 17: Pyroclastic Flow ---
https://adventofcode.com/2022/day/17
"""

from time import perf_counter

TEST = True

DAY = "17"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

NUMBER_OF_ROCKS_I = 2200

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

# ROCKTYPES contains the starting coordinates of each rock shape of the form (x,y)
ROCKTYPES = [
    [(2, 3), (3, 3), (4, 3), (5, 3)],
    [(3, 3), (2, 4), (3, 4), (4, 4), (3, 5)],
    [(2, 3), (3, 3), (4, 3), (4, 4), (4, 5)],
    [(2, 3), (2, 4), (2, 5), (2, 6)],
    [(2, 3), (3, 3), (2, 4), (3, 4)],
]


class Chamber:
    """Model the rock chamber"""

    def __init__(self, width) -> None:
        """Create an empty chamber"""
        self.width = width
        self.heighest_rock = 0
        self.number_rocks_added = 0
        self.formation = set(())
        self.height_increases = []

    def add_new_rock(self, rock_type):
        """Return a new list of the rock's coordinates"""
        new_rock = []
        for coord in ROCKTYPES[rock_type]:
            x, y = coord
            new_rock.append([x, y + self.heighest_rock])
        return new_rock

    def update_rock_position(self, rock, lateral_direction):
        """update the rock's position. A direciton of 0 means drop while -+ 1 is left and right"""
        new_rock_position = []
        for coord in rock:
            x, y = coord
            x += lateral_direction
            if lateral_direction == 0:
                y -= 1
            new_rock_position.append([x, y])
        return new_rock_position

    def test_rock_position(self, rock):
        """test whether the new rock position clashes with the existing rock formation"""
        for coord in rock:
            x, y = coord
            if x < 0 or x > self.width - 1:
                return True
            if tuple(coord) in self.formation:
                return True
            if y < 0:
                return True
        return False

    def add_rock_to_formation(self, rock):
        """Add the rock to the chamber"""
        for coord in rock:
            self.formation.add(tuple(coord))
        self.number_rocks_added += 1
        self.update_heighest_rock()

    def update_heighest_rock(self):
        """work through the formation and extract the heighest rock"""
        current_height = self.heighest_rock
        max_height = 0
        for coord in self.formation:
            x, y = coord
            if y > max_height:
                max_height = y
        self.heighest_rock = max_height + 1
        self.height_increases.append(self.heighest_rock - current_height)

    def display_chamber(self):
        print(self.formation)


def translate_jet(jet):
    """Translate the jet direction"""
    if jet == "<":
        return -1
    else:
        return 1


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def find_repeating_pattern(input_list, period):
    """find whether there is a repeating pattern in the input with the given period"""
    for offset in range(period):
        sub_list_1 = input_list[offset : period + offset]
        sub_list_2 = input_list[period + offset : 2 * period + offset]
        # print(f"list 1 {sub_list_1}\nlist 2 {sub_list_2}")
        if sub_list_1 == sub_list_2:
            print(f"Repeat found with period {period} and offset {offset}")
            break


def main():
    """Main program"""
    gas_jets = get_input_data(FILENAME)[0]
    time_ticker = 0
    my_chamber = Chamber(7)

    for _ in range(NUMBER_OF_ROCKS_I):
        new_rock_number = my_chamber.number_rocks_added % len(ROCKTYPES)
        new_rock = my_chamber.add_new_rock(new_rock_number)
        falling = True
        while falling:
            pointer = time_ticker % len(gas_jets)
            direction = translate_jet(gas_jets[pointer])
            new_position = my_chamber.update_rock_position(new_rock, direction)
            if my_chamber.test_rock_position(new_position):
                pass
            else:
                new_rock = new_position
            new_position = my_chamber.update_rock_position(new_rock, 0)
            time_ticker += 1
            if my_chamber.test_rock_position(new_position):
                my_chamber.add_rock_to_formation(new_rock)
                falling = False
            else:
                new_rock = new_position

    print(f"Part I - Height = {my_chamber.heighest_rock}")

    # following explores the height_increase list to find repeating patterns
    # Part II solved using the outut of this
    for period in range(5, len(my_chamber.height_increases) // 2, 5):
        find_repeating_pattern(my_chamber.height_increases, period)


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
