"""
--- Advent of Code 2022 ---
--- Day 4: Camp Cleanup ---
"""

DAY = "4"
REAL_INPUT = "Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Day" + DAY + "/input_test.txt"
FILENAME = REAL_INPUT


class SectionRange:
    """A range of section numbers"""

    def __init__(self, input_string) -> None:
        """create the section range from the input string (two numbers separeted by '-')"""
        self.input_string = input_string
        self.minimum = int(input_string[: input_string.find("-")])
        self.maximum = int(input_string[input_string.find("-") + 1 :])


class SectionPair:
    """A pair of Section Ranges"""

    def __init__(self, range1, range2) -> None:
        """create the section pair from a pair of ranges"""
        self.range1 = range1
        self.range2 = range2

    def display_range(self):
        print(
            f"""Range1 is {self.range1.minimum} to {self.range1.maximum}
            \nRange1 is {self.range2.minimum} to {self.range2.maximum}"""
        )

    def check_range_containment(self):
        """return true if either range is contained within the other"""
        if (
            self.range1.minimum >= self.range2.minimum
            and self.range1.maximum <= self.range2.maximum
        ):
            return True
        elif (
            self.range2.minimum >= self.range1.minimum
            and self.range2.maximum <= self.range1.maximum
        ):
            return True

    def check_range_overlap(self):
        """return true if there is any overlap between the ranges"""
        if (
            self.range1.minimum >= self.range2.minimum
            and self.range1.minimum <= self.range2.maximum
        ):
            return True
        elif (
            self.range1.maximum >= self.range2.minimum
            and self.range1.maximum <= self.range2.maximum
        ):
            return True
        elif (
            self.range2.maximum >= self.range1.minimum
            and self.range2.maximum <= self.range1.maximum
        ):
            return True
        elif (
            self.range2.minimum >= self.range1.minimum
            and self.range2.minimum <= self.range1.maximum
        ):
            return True


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

    elf_pair_list = []

    for pair in input_data:
        range1 = SectionRange(pair[: pair.find(",")])
        range2 = SectionRange(pair[pair.find(",") + 1 :])
        elf_pair_list.append(SectionPair(range1, range2))

    containment_count = 0
    for pair in elf_pair_list:
        if pair.check_range_containment():
            containment_count += 1

    print(
        f"Part I - number of elf pairs where one range is contained in the other is {containment_count}"
    )

    overlap_count = 0
    for pair in elf_pair_list:
        if pair.check_range_overlap():
            overlap_count += 1

    print(
        f"Part II - number of elf pairs where one range is contained in the other is {overlap_count}"
    )


if __name__ == "__main__":
    main()
