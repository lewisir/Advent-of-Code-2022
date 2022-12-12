"""
--- Advent of Code 2022 ---
--- Day 10: Cathode Ray Tube ---
"""


TEST = False

DAY = "10"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class CpuRegister:
    """Model the CPU Register value"""

    def __init__(self, input_program) -> None:
        """Initialise the Register"""
        self.x = 1
        self.input_program = input_program
        self.value_history = []
        self.process_input_program()

    def process_input_program(self):
        """Process the input signal"""
        self.value_history.append(self.x)
        for line in self.input_program:
            instruction = line.split()[0]
            if instruction == "addx":
                value = int(line.split()[1])
                self.value_history.append(self.x)
                self.x += value
                self.value_history.append(self.x)
            elif instruction == "noop":
                self.value_history.append(self.x)
            else:
                print(f"Error - Unreconised instruction - {instruction}")


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
    my_cpu_register = CpuRegister(input_data)
    signal_strength = 0
    vital_cycles = (20, 60, 100, 140, 180, 220)
    for cycle in vital_cycles:
        signal_strength += cycle * my_cpu_register.value_history[cycle - 1]

    print(f"Part I - Signal Strength {signal_strength}")

    crt_output = ""

    for index, value in enumerate(my_cpu_register.value_history):
        position = index % 40
        print(f"index {index}  \t{position}\t{value}")
        if position == value or position == value - 1 or position == value + 1:
            crt_output += "#"
        else:
            crt_output += " "

    for position in range(0, 239, 40):
        print(crt_output[position : position + 40])


if __name__ == "__main__":
    main()
