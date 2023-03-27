"""
--- Advent of Code 2022 ---
--- Day 17: Pyroclastic Flow ---
https://adventofcode.com/2022/day/17
"""

from time import perf_counter

TEST = False

DAY = "17"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

NUMBER_OF_ROCKS_I = 2022

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

ROCKTYPES = [
    [(2, 3), (3, 3), (4, 3), (5, 3)],
    [(2, 4), (3, 4), (4, 4), (3, 5), (3, 3)],
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

    def add_new_rock(self, rock_type):
        """Return a new list of the rock's coordinates"""
        new_rock = []
        for coord in ROCKTYPES[rock_type]:
            x, y = coord
            new_rock.append([x, y + self.heighest_rock])
        return new_rock

    def update_rock_position(self, rock, lateral_direction):
        """update the rock's position"""
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

    def update_heighest_rock(self):
        """work through the formation and extract the heighest rock"""
        max_height = 0
        for coord in self.formation:
            x, y = coord
            if y > max_height:
                max_height = y
        self.heighest_rock = max_height + 1

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
                my_chamber.update_heighest_rock()
                falling = False
            else:
                new_rock = new_position

    print(f"Part I - Height = {my_chamber.heighest_rock}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
