"""
--- Advent of Code 2022 ---
--- Day 13: Distress Signal ---
"""
TEST = True

DAY = "13"
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


def comapare_packets(packet_left, packet_right):
    """Take in two string literals (that looks like lists) and compated left and right and return whether they are in order or not"""
    pointer_left, pointer_right = 0, 0
    comparing = True
    while comparing:
        if packet_left[pointer_left] == packet_right[pointer_right]:
            pointer_left += 1
            pointer_right += 1
        elif (
            packet_left[pointer_left].isnumeric()
            and packet_right[pointer_right].isnumeric()
        ):
            number_left, pointer_left = get_number(packet_left, pointer_left)
            number_right, pointer_right = get_number(packet_right, pointer_right)
            if number_left < number_right:
                return True
            elif number_left > number_right:
                return False
        elif packet_left[pointer_left].isnumeric():
            return True
        elif packet_right[pointer_right].isnumeric():
            return False


def get_number(packet, pointer):
    """extract an integer from a string"""
    number = ""
    while packet[pointer].isnumeric():
        number += packet[pointer]
        pointer += 1
    return [int(number), pointer]


def insert_brackets(input_string):
    """process the string and if a [] contains a single integer, insert extra [] around if"""
    output_string = ""
    pointer = 0
    for character in input_string:
        if character in "[,]":
            output_string += character
            pointer += 1
        elif character.isnumeric():
            original_pointer = pointer
            number, pointer = get_number(input_string, pointer)
            if (
                input_string[pointer] == "]"
                and input_string[original_pointer - 1] == "["
            ):
                output_string += "[" + str(number) + "]"
            else:
                output_string += str(number)
        else:
            print("Error - unrecognised character")
    return output_string


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    packet_1 = None
    packet_2 = None
    for packet in input_data:
        if packet_1 is None:
            packet_1 = packet
        elif packet_2 is None:
            packet_2 = packet
        elif packet == "":
            print(
                comapare_packets(insert_brackets(packet_1), insert_brackets(packet_2))
            )
            packet_1, packet_2 = None, None


if __name__ == "__main__":
    main()
