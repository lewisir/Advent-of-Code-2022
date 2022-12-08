"""
--- Advent of Code 2022 ---
--- Day 7: No Space Left On Device ---
"""

from cmath import inf

INFINITY = float(inf)

LIMIT = 100000
FILESYSTEMSPACE = 70000000
REQUIREDSPACE = 30000000

TEST = False

DAY = "7"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class Directory_Element:
    """Class to model items in a file structure"""

    def __init__(self, item_name, item_type):
        """initialise the item. the type is either 'FILE' or 'DIR'"""
        self.item_name = item_name
        self.parent_dir = None
        self.item_type = item_type
        self.item_size = None
        self.size_of_contents = None
        self.contents = {}

    def add_item(self, item_key, item):
        """Add an item to the directory"""
        self.contents[item_key] = item

    def content_size(self):
        """calulate the total size of the contents"""
        total_size = 0
        for item in self.contents.values():
            if item.item_type == "DIR":
                total_size += item.content_size()
            elif item.item_type == "FILE":
                total_size += item.item_size
        self.size_of_contents = total_size
        return total_size

    def display_filestructure(self):
        """display the contents"""
        for key, item in self.contents.items():
            if item.item_type == "DIR":
                print(
                    f"dir {item.parent_dir.item_name} dir {item.item_name} size {item.size_of_contents}"
                )
                item.display_filestructure()
            else:
                print(
                    f"dir {item.parent_dir.item_name} file {item.item_name} {item.item_size}"
                )


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def get_line_type(line):
    """determine the type of line: command, directoty or file"""
    sub_string = line[: line.find(" ")]
    if sub_string == "$":
        return "CMD"
    elif sub_string == "dir":
        return "DIR"
    elif sub_string[0] in "123456789":
        return "FILE"
    else:
        return "ERROR - line not recognised"


def process_cmd(line):
    """Given a command line, process the type of command: Change Directory or List"""
    command = line[line.find(" ") + 1 : line.find(" ") + 3]
    if command == "ls":
        return "LS"
    elif command == "cd":
        return "CD"
    else:
        return "ERROR - Command not recognised"


def process_cd_cmd(line):
    """Given a change directory command return the name of the directory"""
    new_dir_name = line[line.find("cd") + 3 :]
    return new_dir_name


def get_file_information(line):
    """Given a file, return the file name and its size"""
    file_size = int(line[: line.find(" ")])
    file_name = line[line.find(" ") + 1 :]
    return [file_name, file_size]


def get_dir_information(line):
    """Given a directory, return the driectoy name"""
    dir_name = line[line.find(" ") + 1 :]
    return dir_name


def build_file_structure(input_data):
    """process the input data and create the file structure"""
    root_directory = Directory_Element("/", "DIR")
    current_dir = root_directory
    for line in input_data:
        if line == "$ cd /":
            line_type = None
        else:
            line_type = get_line_type(line)
            if line_type == "CMD":
                command = process_cmd(line)
                if command == "CD":
                    current_dir_name = process_cd_cmd(line)
                    if current_dir_name == "..":
                        current_dir = current_dir.parent_dir
                    else:
                        current_dir = current_dir.contents[current_dir_name]
                elif command == "LS":
                    pass
                else:
                    print(command)
            elif line_type == "DIR":
                dir_name = get_dir_information(line)
                new_dir = Directory_Element(dir_name, "DIR")
                new_dir.parent_dir = current_dir
                current_dir.add_item(dir_name, new_dir)
            elif line_type == "FILE":
                file_name, file_size = get_file_information(line)
                new_file = Directory_Element(file_name, "FILE")
                new_file.item_size = file_size
                new_file.parent_dir = current_dir
                current_dir.add_item(file_name, new_file)
            else:
                print(line_type)
    return root_directory


def sum_directoy_sizes(directory, limit):
    """sum the contents based on the limit"""
    sum_size = 0
    for key, item in directory.contents.items():
        if item.item_type == "DIR":
            if item.size_of_contents < limit:
                sum_size += item.size_of_contents
            sum_size += sum_directoy_sizes(item, limit)
    return sum_size


def find_directory_size(directory, limit, smallest_size=INFINITY):
    """find the smallest directory that is bigger than the limit"""
    for key, item in directory.contents.items():
        if item.item_type == "DIR":
            if item.size_of_contents > limit and item.size_of_contents < smallest_size:
                smallest_size = item.size_of_contents
                returned_smallest_size = find_directory_size(item, limit, smallest_size)
                if returned_smallest_size < smallest_size:
                    smallest_size = returned_smallest_size
    return smallest_size


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    root_directory = build_file_structure(input_data)
    root_directory.content_size()

    print(f"Part I - {sum_directoy_sizes(root_directory, LIMIT)}")

    total_used_space = root_directory.size_of_contents
    unused_space = FILESYSTEMSPACE - total_used_space
    space_to_free = REQUIREDSPACE - unused_space

    print(
        f"Used Space {total_used_space} and Free Space {unused_space} and need to free {space_to_free}"
    )

    smallest_directory_size = find_directory_size(root_directory, space_to_free)

    print(f"Part II - {smallest_directory_size}")


if __name__ == "__main__":
    main()
