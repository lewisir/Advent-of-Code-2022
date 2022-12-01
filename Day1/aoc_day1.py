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

    current_calorie_count = 0
    elf_calorie_list = []
    for calorie in file_data:
        if calorie == "":
            elf_calorie_list.append(current_calorie_count)
            current_calorie_count = 0
        else:
            current_calorie_count += int(calorie)
    elf_calorie_list.sort(reverse=True)
    top_three_sum = sum(elf_calorie_list[0:3])
    print(
        f"Part I - Elf carrying the most calories is carrying {elf_calorie_list[0]} calories"
    )
    print(f"Part II - Total calories carried by the top three Elves - {top_three_sum}")


if __name__ == "__main__":
    main()
