"""
--- Advent of Code 2022 ---
--- Day 9: Rope Bridge ---
"""


TEST = False

DAY = "9"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

TAIL_MOVE_MATRIX = {
    (-2, -2): (-1, -1),
    (-2, -1): (-1, -1),
    (-2, 0): (-1, 0),
    (-2, 1): (-1, 1),
    (-2, 2): (-1, 1),
    (-1, -2): (-1, -1),
    (-1, 2): (-1, 1),
    (0, -2): (0, -1),
    (0, 2): (0, 1),
    (1, -2): (1, -1),
    (1, 2): (1, 1),
    (2, -2): (1, -1),
    (2, -1): (1, -1),
    (2, 0): (1, 0),
    (2, 1): (1, 1),
    (2, 2): (1, 1),
}

MOVE_CONVERSION = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}


class RopeSection:
    """Model the two ends of the rope - Head and Tail - each has coordinates and record the coordinates visited by each"""

    HEAD_MOVE_MATRIX = {"U": ("y", 1), "D": ("y", -1), "L": ("x", -1), "R": ("x", 1)}

    def __init__(self) -> None:
        """Initialise the rope where the Head and Tail both start at coorindates (0,0)"""
        self.head_coords = {
            "x": 0,
            "y": 0,
        }  # I wonder how to change this to make it easier to add moves to the coordinates
        self.tail_coords = {"x": 0, "y": 0}
        self.tail_positions = {
            (0, 0),
        }

    def move_head_old(self, move):
        """Move the head of the rope in the direction and number of steps provided"""  # this was the original (Part I) way I solved the problem
        direction, distance = move
        direct_coord, step_value = self.HEAD_MOVE_MATRIX[direction]
        for _ in range(distance):
            self.head_coords[direct_coord] += step_value
            self.update_tail()

    def move_head(self, move):
        """ "Move the head of the rope section"""
        self.head_coords["x"] += move[0]
        self.head_coords["y"] += move[1]
        self.update_tail()

    def relative_position(self):
        """return the relative position of the Head from the Tail"""
        return (
            self.head_coords["x"] - self.tail_coords["x"],
            self.head_coords["y"] - self.tail_coords["y"],
        )

    def update_tail(self):
        """update the position of the tail based on the position of the head of the rope"""
        relative_coords = self.relative_position()
        if abs(relative_coords[0]) > 1 or abs(relative_coords[1]) > 1:
            tail_move = TAIL_MOVE_MATRIX[relative_coords]
            self.tail_coords["x"] += tail_move[0]
            self.tail_coords["y"] += tail_move[1]
            self.record_tail_position()

    def record_tail_position(self):
        """Add the tail's position to the tail position set"""
        tail_position = (self.tail_coords["x"], self.tail_coords["y"])
        self.tail_positions.add(tail_position)

    def display(self):
        """display object data"""
        print(
            f"Head {self.head_coords}, Tail {self.tail_coords}, Tail Positions {self.tail_positions}"
        )


class Rope:
    """Model a rope as multiple RopeSections"""

    def __init__(self, number_of_sections) -> None:
        """Initilise the rope"""
        self.rope_sections = []
        for _ in range(number_of_sections):
            self.rope_sections.append(RopeSection())

    def move_head(self, move, section=0):
        """Move the head of the rope"""
        self.rope_sections[section].move_head(move)
        if section < len(self.rope_sections) - 1:
            relative_coords = self.relative_coords_between_sections(section)
            if abs(relative_coords[0]) > 1 or abs(relative_coords[1]) > 1:
                tail_move = TAIL_MOVE_MATRIX[relative_coords]
                self.move_head(tail_move, section + 1)

    def relative_coords_between_sections(self, section=0):
        """return the relative position of the Head from the Tail"""
        return (
            self.rope_sections[section].tail_coords["x"]
            - self.rope_sections[section + 1].head_coords["x"],
            self.rope_sections[section].tail_coords["y"]
            - self.rope_sections[section + 1].head_coords["y"],
        )

    def display(self):
        """Display the rope's positions"""
        for index, rope in enumerate(self.rope_sections):
            print(f"Rope Section {index}")
            rope.display()


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_input_data(input_data):
    """process the input data and return a list of the moves"""
    move_list = []
    for line in input_data:
        direction, distance = line.split()
        move_list.append((direction, int(distance)))
    return move_list


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    move_list = process_input_data(input_data)
    my_rope = RopeSection()
    for move in move_list:
        for _ in range(move[1]):
            my_rope.move_head(MOVE_CONVERSION[move[0]])

    print(f"Part I - number of Tail positions is {len(my_rope.tail_positions)}")

    my_rope = Rope(5)
    for move in move_list:
        for _ in range(move[1]):
            my_rope.move_head(MOVE_CONVERSION[move[0]])

    print(
        f"Part II - number of Tail positions of the end of the rope {len(my_rope.rope_sections[-1].tail_positions)}"
    )


if __name__ == "__main__":
    main()
