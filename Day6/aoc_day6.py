"""
--- Advent of Code 2022 ---
--- Day 6: Tuning Trouble ---
"""

TEST = False

DAY = "6"
REAL_INPUT = "Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Day" + DAY + "/input_test.txt"


WINDOW = 14

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

def check_unique_characters(input_string):
    """check if the input string contains no repeated characters"""
    for position, char in enumerate(input_string):
        if char in input_string[position+1:]:
            return False
    return True

def main():
    """Main program"""
    input_data = get_input_data(FILENAME)

    TEST_STRING = input_data[0]

    for position in range(len(TEST_STRING)):
        sub_string = TEST_STRING[position:position+WINDOW]
        if check_unique_characters(sub_string):
            print(f"Position for first {WINDOW} distinct characters {position+WINDOW}")
            break


if __name__ == "__main__":
    main()
