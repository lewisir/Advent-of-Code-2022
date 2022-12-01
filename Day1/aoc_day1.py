"""
--- Advent of Code 2022 ---
--- Day 1: Calorie Counting ---
"""


def main():
    """Main program"""
    filename = "Day1/input_day1.txt"
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))

    highest_calorie_count = 0
    current_calorie_count = 0

    for calorie in file_data:
        if calorie == "":
            if current_calorie_count > highest_calorie_count:
                highest_calorie_count = current_calorie_count
            current_calorie_count = 0
        else:
            current_calorie_count += int(calorie)
    print(
        f"Part I - Elf carrying the most calories is carrying {highest_calorie_count} calories"
    )


if __name__ == "__main__":
    main()
