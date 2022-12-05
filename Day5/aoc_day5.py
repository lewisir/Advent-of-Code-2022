"""
--- Advent of Code 2022 ---
--- Day 5: Supply Stacks ---
"""

TEST = True

DAY = "5"
REAL_INPUT = "Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class CrateStack:
    """model a stack of crates"""

    def __init__(self) -> None:
        self.stack = []

    def top_crate(self):
        """return the crate at the top of the stack"""
        return self.stack[-1]

    def add_crate(self, crate):
        """add a crate to the top of the stack"""
        self.stack.append(crate)

    def add_multiple_crates(self, crates):
        """add the set of crates to the stack. The set of crates provided is iteslf a stack (list) of crates"""
        self.stack.extend(crates)

    def remove_crate(self):
        """remove a crate from the stack and return its value"""
        crate = self.stack.pop()
        return crate

    def remove_multiple_crates(self, number_of_crates):
        """remove the number of crates from the top of the stack."""
        little_stack = self.stack[-number_of_crates:]
        for _ in range(number_of_crates):
            self.stack.pop()
        return little_stack

    def display_stack(self):
        """print out the stack of crates (bottom to top)"""
        print(f"{self.stack}")


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def initialise_test_stacks():
    stack_dict = {}
    for stack_id in range(1, 4):
        stack_dict[stack_id] = CrateStack()
    for crate in ["Z", "N"]:
        stack_dict[1].add_crate(crate)
    for crate in ["M", "C", "D"]:
        stack_dict[2].add_crate(crate)
    for crate in ["P"]:
        stack_dict[3].add_crate(crate)
    return stack_dict


def initialise_stacks():
    stack_dict = {}
    for stack_id in range(1, 10):
        stack_dict[stack_id] = CrateStack()
    for crate in ["B", "P", "N", "Q", "H", "D", "R", "T"]:
        stack_dict[1].add_crate(crate)
    for crate in ["W", "G", "B", "J", "T", "V"]:
        stack_dict[2].add_crate(crate)
    for crate in ["N", "R", "H", "D", "S", "V", "M", "Q"]:
        stack_dict[3].add_crate(crate)
    for crate in ["P", "Z", "N", "M", "C"]:
        stack_dict[4].add_crate(crate)
    for crate in ["D", "Z", "B"]:
        stack_dict[5].add_crate(crate)
    for crate in ["V", "C", "W", "Z"]:
        stack_dict[6].add_crate(crate)
    for crate in ["G", "Z", "N", "C", "V", "Q", "L", "S"]:
        stack_dict[7].add_crate(crate)
    for crate in ["L", "G", "J", "M", "D", "N", "V"]:
        stack_dict[8].add_crate(crate)
    for crate in ["T", "P", "M", "F", "Z", "C", "G"]:
        stack_dict[9].add_crate(crate)
    return stack_dict


def move_crates(from_stack, to_stack, number_of_crates):
    for _ in range(number_of_crates):
        crate = from_stack.remove_crate()
        to_stack.add_crate(crate)


def move_multiple_crates(from_stack, to_stack, number_of_crates):
    crates = from_stack.remove_multiple_crates(number_of_crates)
    to_stack.add_multiple_crates(crates)


def display_stacks(stack_dict):
    for stack in stack_dict:
        stack_dict[stack].display_stack()


def extract_move(move_command):
    number_start = move_command.find("move") + 5
    number_end = move_command.find("from") - 1
    from_start = move_command.find("from") + 5
    from_end = move_command.find("to") - 1
    to_start = move_command.find("to") + 3
    to_end = len(move_command)
    number_of_crates = int(move_command[number_start:number_end])
    from_stack = int(move_command[from_start:from_end])
    to_stack = int(move_command[to_start:to_end])
    return [from_stack, to_stack, number_of_crates]


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)

    if TEST:
        stack_dict = initialise_test_stacks()
    else:
        stack_dict = initialise_stacks()

    move_commands = input_data
    move_list = []
    for move in move_commands:
        move_list.append(extract_move(move))

    for move in move_list:
        from_crate = move[0]
        to_crate = move[1]
        number_of_crates = move[2]
        move_crates(stack_dict[from_crate], stack_dict[to_crate], number_of_crates)

    top_crates = ""
    for stack in stack_dict:
        top_crates += stack_dict[stack].top_crate()

    print(f"Part I - The top crates are {top_crates}")

    if TEST:
        stack_dict = initialise_test_stacks()
    else:
        stack_dict = initialise_stacks()

    for move in move_list:
        from_crate = move[0]
        to_crate = move[1]
        number_of_crates = move[2]
        move_multiple_crates(
            stack_dict[from_crate], stack_dict[to_crate], number_of_crates
        )

    top_crates = ""
    for stack in stack_dict:
        top_crates += stack_dict[stack].top_crate()

    print(f"Part II - The top crates are {top_crates}")


if __name__ == "__main__":
    main()
