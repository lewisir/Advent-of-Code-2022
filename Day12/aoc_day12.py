"""
--- Advent of Code 2022 ---
--- Day 12: Hill Climbing Algorithm ---
"""
from cmath import inf
from time import perf_counter


TEST = False

DAY = "12"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class HeightMap:
    """Model the height map"""

    CHARPRIORITY = "abcdefghijklmnopqrstuvwxyz"
    HOPCOST = 1

    def __init__(self, heightmap) -> None:
        """Initialise the height map"""
        self.heightmap = heightmap
        self.y_size = len(self.heightmap)
        self.x_size = len(self.heightmap[0])
        self.src_coord = self.find_starting_point()
        self.dst_coord = self.find_ending_point()
        self.dfs_visited = set()

    def find_starting_point(self):
        """Find the starting point, S"""
        for y, row in enumerate(self.heightmap):
            for x, height in enumerate(row):
                if height == "S":
                    source_coord = (y, x)
        return source_coord

    def find_ending_point(self):
        """Find the ending point, E"""
        for y, row in enumerate(self.heightmap):
            for x, height in enumerate(row):
                if height == "E":
                    dest_coord = (y, x)
        return dest_coord

    def all_possible_start_points(self, start_char):
        """compile a list of all possible starting points"""
        all_start_points = []
        for y, row in enumerate(self.heightmap):
            for x, height in enumerate(row):
                if height == start_char:
                    all_start_points.append((y, x))
        return all_start_points

    def spf(self, start, end) -> int:
        """
        Calculate the lowest cost path between the start and end coordinates
        Return the cost of the lowest cost path
        """
        # Mark points (nodes) in the map as unvisited as they are examined
        # Assign to every point a Tentative Distance initialised to infinity
        # Set the starting node as current and its tenative distance to 0
        unvisited_nodes = {start, end}
        node_distances = self.initialise_distances()
        current_node = start
        node_distances[current_node] = 0

        # For the current node consider its unvisited neighbours
        # Calculate for each unvisited neighbour its tentative distance through the current node
        # Compare new tentative distance with the current one and assign the smaller distance
        # Once all unvisited neighbours are processed, mark the current node as visited
        # If destination node has been marked visited then stop
        # Else select the unvisited node with the smallest tentative distance and set as current and LOOP
        while end in unvisited_nodes:
            current_node_distance = node_distances[current_node]
            current_neighbours = self.get_nodes_neighbours(current_node)
            for neighbour in current_neighbours:
                if node_distances[neighbour] == float(inf):
                    unvisited_nodes.add(neighbour)
                if neighbour in unvisited_nodes:
                    neighbour_tenative_distance = current_node_distance + self.HOPCOST
                    if neighbour_tenative_distance < node_distances[neighbour]:
                        node_distances[neighbour] = neighbour_tenative_distance
            unvisited_nodes.remove(current_node)
            if current_node == end:
                break
            else:
                current_node = self.get_next_closest_node(
                    unvisited_nodes, node_distances
                )
        # print(f"Number of visited nodes {self.number_of_visted_nodes(node_distances)}")
        return node_distances[end]

    def initialise_distances(self):
        """
        Function to create a dictionary of all nodes and initialise the distances to infinity
        Each key is a Tuple of the y and x coordinates
        Each value is infinity
        """
        node_distances = {}
        for y in range(self.y_size):
            for x in range(self.x_size):
                node_distances[(y, x)] = float(inf)
        return node_distances

    def get_nodes_neighbours(self, node):
        """Return a ist of the node's neighbours' coordinates"""
        neighbour_list = []
        y_coord, x_coord = node
        height = self.heightmap[y_coord][x_coord]
        if y_coord != 0:
            neighbour_height = self.heightmap[y_coord - 1][x_coord]
            if self.compare_neighbour_heights(height, neighbour_height):
                neighbour_list.append((y_coord - 1, x_coord))
        if y_coord != self.y_size - 1:
            neighbour_height = self.heightmap[y_coord + 1][x_coord]
            if self.compare_neighbour_heights(height, neighbour_height):
                neighbour_list.append((y_coord + 1, x_coord))
        if x_coord != 0:
            neighbour_height = self.heightmap[y_coord][x_coord - 1]
            if self.compare_neighbour_heights(height, neighbour_height):
                neighbour_list.append((y_coord, x_coord - 1))
        if x_coord != self.x_size - 1:
            neighbour_height = self.heightmap[y_coord][x_coord + 1]
            if self.compare_neighbour_heights(height, neighbour_height):
                neighbour_list.append((y_coord, x_coord + 1))
        return neighbour_list

    def get_next_closest_node(self, unvisited_nodes, node_distances):
        """Return the node with the smallest distance from the unvisited nodes"""
        smallest_distance = float(inf)
        current_node = None
        for node in unvisited_nodes:
            if current_node is None:
                current_node = node
            if node_distances[node] < smallest_distance:
                smallest_distance = node_distances[node]
                current_node = node
        return current_node

    def compare_neighbour_heights(self, height, neighbour_height):
        if height == "S":
            height = "a"
        if height == "E":
            height = "z"
        if neighbour_height == "S":
            neighbour_height = "a"
        if neighbour_height == "E":
            neighbour_height = "z"
        if (
            self.CHARPRIORITY.find(neighbour_height)
            <= self.CHARPRIORITY.find(height) + 1
        ):
            return True
        else:
            return False


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
    my_heightmap = HeightMap(input_data)
    print(
        f"Part I - shortest distance from S to E is {my_heightmap.spf(my_heightmap.src_coord, my_heightmap.dst_coord)}"
    )
    print(f"-- Time Taken {perf_counter() - start_time}")
    least_cost = float(inf)
    start_point_list = my_heightmap.all_possible_start_points("a")
    for start in start_point_list:
        cost = my_heightmap.spf(start, my_heightmap.dst_coord)
        if cost < least_cost:
            least_cost = cost
    print(f"Part II - Least cost to any start position is {least_cost}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
