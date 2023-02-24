"""
--- Advent of Code 2022 ---
--- Day 16: Proboscidea Volcanium ---
https://adventofcode.com/2022/day/16
"""
TEST = True

DAY = "16"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

TIME = 30

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

from cmath import inf
from time import perf_counter


class Valve:
    """Model a pressure release Valve"""

    def __init__(self, location, rate):
        self.location = location
        self.rate = rate
        self.vectors = {}
        self.open = False


class ValvePath:
    """Model a sequence of opening valves"""

    def __init__(self) -> None:
        self.path = []

    @property
    def path_length(self):
        """calculate and return the length of the path"""
        length = 0
        for valve in self.path:
            length += valve[1]
        return length

    @property
    def path_valves(self):
        """calculate and return the number of valves in the path"""
        return len(self.path)

    def path_flow(self, time):
        """calcualte the total flow the path allows from the given time"""
        flow_rate = 0
        total_flow = 0
        for valve in self.path:
            if time > valve[1] + 1:
                time -= valve[1] + 1
                total_flow += flow_rate * (valve[1] + 1)
                flow_rate += valve[0].rate
            else:
                break
        total_flow += flow_rate * time
        return total_flow

    def add_valve(self, valve_tuple):
        """
        The valve tuple is ('valve', distance)
        valve is the Valve object
        distance is the time taken to reach this valve from the preceeding one in the path
        """
        self.path.append(valve_tuple)

    def pop_last_valve(self):
        """remove the last entry from the path"""
        self.path.pop()

    def display_path(self, time):
        """Print out the path"""
        for valve in self.path:
            print(f"({valve[0].location},{valve[1]})", end="")
        print(f" - {self.path_flow(time)}")

    def reset_path(self):
        """Clear the path list"""
        self.path = []


class TunnelMap:
    """Model the tunnels between the valves"""

    HOPCOST = 1

    def __init__(self, tunnel_map):
        self.tunnel_map = tunnel_map

    def compute_path(self, source):
        """Given the source, calculate the distance to each other location"""

    def spf(self, source):
        """Run SPF and return a dictionary of all the destinations and their distances from the soure"""
        unvisited_nodes = set(())
        for node in self.tunnel_map:
            unvisited_nodes.add(node)
        node_distances = self.initialise_distances()
        current_node = source
        node_distances[current_node] = 0
        while len(unvisited_nodes) > 0:
            current_node_distance = node_distances[current_node]
            current_neighbours = self.tunnel_map[current_node]
            for neighbour in current_neighbours:
                if neighbour in unvisited_nodes:
                    neighbour_tenative_distance = current_node_distance + self.HOPCOST
                    if neighbour_tenative_distance < node_distances[neighbour]:
                        node_distances[neighbour] = neighbour_tenative_distance
            unvisited_nodes.remove(current_node)
            current_node = self.get_next_closest_node(unvisited_nodes, node_distances)
        return node_distances

    def initialise_distances(self):
        """Set all nodes' distances to infinity"""
        node_distances = {}
        for node in self.tunnel_map:
            node_distances[node] = float(inf)
        return node_distances

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


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def get_valve_data(input_data):
    """Process the input data and get the valve information"""
    valve_dict = {}
    for line in input_data:
        valve = line[6:8]
        rate = int(line[line.find("rate=") + 5 : line.find(";")])
        valve_dict[valve] = Valve(valve, rate)
    return valve_dict


def get_tunnel_data(input_data):
    """Process the input data and build the tunnel connections"""
    tunnel_dict = {}
    for line in input_data:
        valve = line[6:8]
        temp_string = line[line.find("to valve") :]
        tunnel_dict[valve] = [x.rstrip(",") for x in temp_string.split()[2:]]
    tunnel_map = TunnelMap(tunnel_dict)
    return tunnel_map


def update_valve_vectors(valve_dict, tunnel_map):
    """add the vectors for each valve"""
    for name, valve in valve_dict.items():
        valve.vectors = tunnel_map.spf(name)


def get_viable_valves(path, time, valve_dict):
    """
    get a list of the viable valves from the last valve in the path given  the remaining time
    viable valves are within range and not already in the path
    """
    current_valve = path.path[-1][0]
    visited_valves = []
    for valve_tuple in path.path:
        visited_valves.append(valve_tuple[0])
    viable_valves = []
    for name, valve in valve_dict.items():
        distance = valve_dict[current_valve.location].vectors[name]
        if valve not in visited_valves and distance <= (time - 2) and valve.rate > 0:
            viable_valves.append((valve, distance))
    return viable_valves


def discover_paths(source, time, valve_dict, path=ValvePath(), all_paths=[]):
    """discover all paths between valves"""
    path.add_valve(source)
    next_nodes = get_viable_valves(path, time, valve_dict)
    if len(next_nodes) == 0:
        new_path = ValvePath()
        for valve in path.path:
            new_path.add_valve(valve)
        total_flow = new_path.path_flow(TIME)
        all_paths.append(total_flow)
        return all_paths
    for node in next_nodes:
        discover_paths(node, time - path.path[-1][1], valve_dict, path, all_paths)
        path.pop_last_valve()
    return all_paths


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    all_valve_dict = get_valve_data(input_data)
    tunnel_map = get_tunnel_data(input_data)

    update_valve_vectors(all_valve_dict, tunnel_map)

    valve_dict = {}
    for name, valve in all_valve_dict.items():
        if valve.rate > 0:
            valve_dict[name] = valve

    max_flows = []
    for name, valve in valve_dict.items():
        temp_path = ValvePath()
        if valve.rate != 0:
            flow_rates = discover_paths(
                (valve, valve.vectors["AA"]), TIME, valve_dict, temp_path
            )
            max_flows.append(max(flow_rates))
        del temp_path
    print(f"Max Flow Found {max(max_flows)}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
