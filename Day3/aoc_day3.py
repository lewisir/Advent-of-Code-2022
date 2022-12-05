"""
--- Advent of Code 2022 ---
--- Day 3: Rucksack Reorganization ---
"""

DAY = "3"
REAL_INPUT = "Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Day" + DAY + "/input_test.txt"
filename = REAL_INPUT


class Rucksack:
    """Models a Rucksak with two compartments"""

    def __init__(self, rucksack_contents):
        """Initialise the rucksak with an input string"""
        self.contents = rucksack_contents
        self.total_items = len(self.contents)
        self.compartment_items_count = self.total_items // 2
        self.compartment_1_contents = self.contents[: self.compartment_items_count]
        self.compartment_2_contents = self.contents[self.compartment_items_count :]
        self.common_compartment_item = self.find_common_item()

    def find_common_item(self):
        """find the item common to both compartments"""
        for item in self.compartment_1_contents:
            if item in self.compartment_2_contents:
                return item


def get_item_priority(item):
    items = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for index, element in enumerate(items):
        if element == item:
            return index + 1


def main():
    """Main program"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))

    elf_rucksacks = []
    for line in file_data:
        elf_rucksacks.append(Rucksack(line))

    priority_sum = 0

    for rucksack in elf_rucksacks:
        rucksack.find_common_item()
        priority_sum += get_item_priority(rucksack.common_compartment_item)

    print(f"Part I - Sum of priorities for common items is {priority_sum}")

    priority_sum = 0

    for x in range(0, len(file_data), 3):
        elf_group = file_data[x : x + 3]
        for item in elf_group[0]:
            if item in elf_group[1]:
                if item in elf_group[2]:
                    priority_sum += get_item_priority(item)
                    break

    print(
        f"Part II - Sum of priorities for items common in each elf group is {priority_sum}"
    )


if __name__ == "__main__":
    main()
