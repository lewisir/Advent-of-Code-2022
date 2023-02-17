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
from itertools import permutations
from time import perf_counter


class Valve:
    """Model a pressure release Valve"""

    def __init__(self, location, rate):
        self.location = location
        self.rate = rate
        self.open = False


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


def calculate_flow(valve_sequence, valve_dict, tunnel_map, time, start_location="AA"):
    """Given a sequnece of valves and the time calculate the total flow"""
    total_rate = 0
    total_flow = 0
    distance_to_next_valve = 0
    moving = False
    current_location = start_location
    while time > 0:
        if len(valve_sequence) > 0 and moving is False:
            next_valve = valve_sequence.pop(0)
            distance_to_next_valve = tunnel_map.spf(current_location)[next_valve]
            moving = True
        time -= 1
        total_flow += total_rate
        if distance_to_next_valve > 0:
            distance_to_next_valve -= 1
        else:
            moving = False
            current_location = next_valve
            if valve_dict[current_location].open is False:
                valve_dict[current_location].open = True
                total_rate += valve_dict[current_location].rate
    return total_flow


def next_reachable_valves(start_valve, remaining_time, open_valves):
    """Return a dictionary of reachable valves and their distances"""
    reachable_valves = {}
    for valve, distance in open_valves.items():
        if distance < remaining_time:
            reachable_valves[valve] = distance
    return reachable_valves


def get_open_valves(start_valve, valve_dict, tunnel_map):
    """return a dictionary of the open valves and their distances"""
    open_valves = {}
    for valve in valve_dict:
        if valve_dict[valve].open:
            distance = tunnel_map.spf(start_valve)[valve]
            open_valves[valve] = distance
    return open_valves


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    valve_dict = get_valve_data(input_data)
    tunnel_map = get_tunnel_data(input_data)

    valve_list = []
    for valve_name, valve in valve_dict.items():
        if valve.rate > 0:
            valve_list.append(valve_name)

    max_flow = 0
    calculated_combinations = 0

    for combination in permutations(valve_list, 6):
        combination = list(combination)
        flow = calculate_flow(combination, valve_dict, tunnel_map, TIME)
        calculated_combinations += 1
        if flow > max_flow:
            max_flow = flow
            optimum_sequence = combination
        for valve in valve_dict:
            valve_dict[valve].open = False

    print(f"Max Flow is {max_flow}\nHaving run {calculated_combinations} combinations")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
