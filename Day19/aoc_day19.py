"""
--- Advent of Code 2022 ---
--- Day 19: Not Enough Minerals ---
https://adventofcode.com/2022/day/19
"""

from time import perf_counter

TEST = True

DAY = "19"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class Factory:
    """Model a factory that is based on a blueprint"""

    def __init__(self, blueprint):
        """Initialise the Factory"""
        self.name = blueprint["name"]
        self.minerals = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        self.robots = {"O": 1, "C": 0, "B": 0, "G": 0}
        self.robot_costs = {
            "O": {"ore": blueprint["ore"], "clay": 0, "obsidian": 0},
            "C": {"ore": blueprint["clay"], "clay": 0, "obsidian": 0},
            "B": {
                "ore": blueprint["obsidian"][0],
                "clay": blueprint["obsidian"][1],
                "obsidian": 0,
            },
            "G": {
                "ore": blueprint["geode"][0],
                "clay": 0,
                "obsidian": blueprint["geode"][1],
            },
        }

    def create_robot(self, robot):
        """Create a robot of the given type 'O', 'C', 'B' or 'G'"""
        self.minerals["ore"] -= self.robot_costs[robot]["ore"]
        self.minerals["clay"] -= self.robot_costs[robot]["clay"]
        self.minerals["obsidian"] -= self.robot_costs[robot]["obsidian"]
        self.robots[robot] += 1

    def gather_minerals(self, new_robot="N"):
        """Update the minerals gathered. The new_robot is used to control whether that mineral is updated"""
        self.minerals["ore"] += self.robots["O"]
        self.minerals["clay"] += self.robots["C"]
        self.minerals["obsidian"] += self.robots["B"]
        self.minerals["geode"] += self.robots["G"]

    def display_factory(self):
        """Display the state of the factory"""
        print(f"Blueprint # {self.name}")
        print(f"Ore Robots cost {self.robot_costs['O']} ore")
        print(f"Clay Robots cost {self.robot_costs['C']} ore")
        print(
            f"Obsidian Robots cost {self.robot_costs['O']} ore and {self.robot_costs['C']} clay"
        )
        print(
            f"Geode Robots cost {self.robot_costs['O']} ore and {self.robot_costs['B']} obsidian"
        )
        self.display_inventory()

    def display_inventory(self):
        """Display the inventory of the factory"""
        print(f"\tOre\tClay\tObsidn\tGeodes")
        print(
            f"Minrls\t{self.minerals['ore']}\t{self.minerals['clay']}\t{self.minerals['obsidian']}\t{self.minerals['geode']}"
        )
        print(
            f"Robots\t{self.robots['O']}\t{self.robots['C']}\t{self.robots['B']}\t{self.robots['G']}"
        )


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_blueprint_data(blueprint_data):
    """Process the blueprint data and return a list of blueprints (dictionaries)"""
    blueprints = []
    for blueprint in blueprint_data:
        blueprint_dict = {
            "name": int(blueprint.split()[1][0]),
            "ore": int(blueprint.split()[6]),
            "clay": int(blueprint.split()[12]),
            "obsidian": [int(blueprint.split()[18]), int(blueprint.split()[21])],
            "geode": [int(blueprint.split()[27]), int(blueprint.split()[30])],
        }
        blueprints.append(Factory(blueprint_dict))
    return blueprints


def get_next_robots():
    """identify the viable next robots"""
    return None


def build_robot_sequence(robot, robot_sequence, time, factory, robot_sequences=[]):
    """Discover all the possible build orders of the robots"""
    robot_sequence += robot
    next_robots = get_next_robots(time, factory)
    if time == 0:
        return robot_sequences.append(robot_sequence)
    for robot in next_robots:
        factory.create_robot(robot)
    return None


def main():
    """Main program"""
    my_factories = process_blueprint_data(get_input_data(FILENAME))
    factory = my_factories[0]
    for _ in range(9):
        factory.gather_minerals()
        factory.create_robot("O")
    factory.display_factory()


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
