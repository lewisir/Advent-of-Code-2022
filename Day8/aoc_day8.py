"""
--- Advent of Code 2022 ---
--- Day 8: Treetop Tree House ---
"""


TEST = False

DAY = "8"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class TreeArray:
    """Model an array of trees each having a single digit integer height"""

    def __init__(self, tree_array):
        """Initialise the Tree Array. The input data is a 2D array of integers"""
        self.tree_array = tree_array
        self.depth = len(self.tree_array)
        self.width = len(self.tree_array[0])
        self.visible_trees = 2 * (self.depth + self.width - 2) + self.copse_visibility()
        self.most_scenic_tree = self.copse_scenicity()

    def display(self):
        """A nice way to print the array"""
        SPACE = " "
        for row in self.tree_array:
            print(f"{SPACE.join(map(str,row))}")

    def check_tree_visibility(self, tree_height, tree_row):
        """check if the tree can be seen compared to the row of trees"""
        max_height = 0
        for tree in tree_row:
            if tree > max_height:
                max_height = tree
        if tree_height <= max_height:
            return False
        return True

    def count_until_next_tree(self, tree_height, tree_row):
        """count the number of trees in the row until a tree of the same or greater height is found"""
        tree_count = 0
        for tree in tree_row:
            if tree < tree_height:
                tree_count += 1
            else:
                tree_count += 1
                return tree_count
        return tree_count

    def extract_tree_rows(self, i, j, towards_tree_flag=True):
        """get the partial rows of trees for a tree at position i, j"""
        sub_row_left = self.tree_array[i][:j]
        if not towards_tree_flag:
            sub_row_left.reverse()
        sub_row_right = self.tree_array[i][j + 1 :]
        if towards_tree_flag:
            sub_row_right.reverse()
        sub_row_up = []
        for x in range(0, i):
            sub_row_up.append(self.tree_array[x][j])
        if not towards_tree_flag:
            sub_row_up.reverse()
        sub_row_down = []
        for x in range(i + 1, self.depth):
            sub_row_down.append(self.tree_array[x][j])
        if towards_tree_flag:
            sub_row_down.reverse()
        return [sub_row_left, sub_row_right, sub_row_up, sub_row_down]

    def copse_visibility(self):
        """ "work through the copse and calcualte the total number of visible tress"""
        visible_trees = 0
        for i in range(1, self.depth - 1):
            for j in range(1, self.width - 1):
                tree_height = self.tree_array[i][j]
                test_rows = self.extract_tree_rows(i, j)
                for row in test_rows:
                    if self.check_tree_visibility(tree_height, row):
                        visible_trees += 1
                        break
        return visible_trees

    def copse_scenicity(self):
        """work through the copses and find the most scenic value"""
        most_scenic_tree = 0
        for i in range(1, self.depth - 1):
            for j in range(1, self.width - 1):
                tree_height = self.tree_array[i][j]
                test_rows = self.extract_tree_rows(i, j, False)
                tree_scenic_value = 1
                for row in test_rows:
                    scenic_component = self.count_until_next_tree(tree_height, row)
                    tree_scenic_value *= scenic_component
                if tree_scenic_value > most_scenic_tree:
                    most_scenic_tree = tree_scenic_value
        return most_scenic_tree


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_string_to_int_list(input_string):
    """Process the input string and conver to a list of separate integers"""
    output_list = []
    for char in input_string:
        output_list.append(int(char))
    return output_list


def display_array(array):
    """A nice wayt o print the array"""
    SPACE = " "
    for row in array:
        print(f"{SPACE.join(map(str,row))}")


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    array = []
    for line in input_data:
        array.append(process_string_to_int_list(line))

    tree_array = TreeArray(array)

    print(f"Part I - visble trees = {tree_array.visible_trees}")
    print(f"Part II - most scenic tree value = {tree_array.most_scenic_tree}")


if __name__ == "__main__":
    main()
