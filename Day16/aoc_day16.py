"""
--- Advent of Code 2022 ---
--- Day 16: Proboscidea Volcanium ---
https://adventofcode.com/2022/day/16
"""
TEST = False

DAY = "16"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"

# Set time to 30 for part I and 26 for part II
TIME = 26
INF = float("inf")
TIME_TO_SWITCH_ON_VALVE = 1

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

from time import perf_counter
from itertools import combinations


class Valve:
    """Model a pressure release Valve"""

    def __init__(self, location, rate):
        self.location = location
        self.rate = rate
        self.vectors = {}
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
            node_distances[node] = INF
        return node_distances

    def get_next_closest_node(self, unvisited_nodes, node_distances):
        """Return the node with the smallest distance from the unvisited nodes"""
        smallest_distance = INF
        current_node = None
        for node in unvisited_nodes:
            if current_node is None:
                current_node = node
            if node_distances[node] < smallest_distance:
                smallest_distance = node_distances[node]
                current_node = node
        return current_node


class ValvePath:
    """Model a sequence of opening valves"""

    def __init__(self) -> None:
        self.path = []

    def path_length(self, current_valve):
        """calculate and return the length of the path"""
        length = 0
        for valve in self.path:
            length += current_valve.vectors[valve.location]
            current_valve = valve
        return length

    def path_valves(self):
        """calculate and return the number of valves in the path"""
        return len(self.path)

    def add_valve(self, valve):
        """add a valve to the path"""
        self.path.append(valve)

    def pop_last_valve(self):
        """remove the last entry from the path"""
        self.path.pop()

    def display_path(self):
        """Print out the path"""
        for valve in self.path:
            print(f"{valve.location}", end="")
        print()

    def reset_path(self):
        """Clear the path list"""
        self.path = []

    def path_flow(self, time, current_valve):
        """calculate the total flow the path allows from the given time"""
        flow_rate = 0
        total_flow = 0
        for valve in self.path:
            if time > current_valve.vectors[valve.location] + 1:
                time -= current_valve.vectors[valve.location] + 1
                total_flow += flow_rate * (current_valve.vectors[valve.location] + 1)
                flow_rate += valve.rate
                current_valve = valve
            else:
                break
        total_flow += flow_rate * time
        return total_flow


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


def get_viable_valves(current_valve, time, valve_dict, visited_valves):
    """
    get a list of the viable valves from a location given the remaining time
    viable valves are within range and not already visited
    """
    viable_valves = []
    for name, valve in valve_dict.items():
        distance = valve_dict[current_valve.location].vectors[name]
        if valve not in visited_valves and distance < (time - 1) and valve.rate > 0:
            viable_valves.append(valve)
    return viable_valves


def discover_path(source, time, valve_dict, path, visited_valves=set(()), all_paths=[]):
    """discover all paths between valves"""
    path.add_valve(source)
    visited_valves.add(source)
    next_nodes = get_viable_valves(source, time, valve_dict, visited_valves)
    if len(next_nodes) == 0:
        new_flow = path.path_flow(TIME, valve_dict["AA"])
        all_paths.append(new_flow)
        return all_paths
    for node in next_nodes:
        updated_time = time - source.vectors[node.location] - TIME_TO_SWITCH_ON_VALVE
        if updated_time >= 1:
            discover_path(
                node,
                updated_time,
                valve_dict,
                path,
                visited_valves,
                all_paths,
            )
            path.pop_last_valve()
            visited_valves.discard(node)
    return all_paths


def work_through_valve_list(valves):
    all_flows = []
    for valve in valves.values():
        temp_path = ValvePath()
        visited_valves = set(())
        if valve.rate != 0:
            new_flow_list = discover_path(
                valve, TIME - valve.vectors["AA"], valves, temp_path, visited_valves, []
            )
            all_flows.extend(new_flow_list)
        del temp_path
    return all_flows


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    all_valve_dict = get_valve_data(input_data)
    tunnel_map = get_tunnel_data(input_data)
    update_valve_vectors(all_valve_dict, tunnel_map)

    useable_valves = {"AA": all_valve_dict["AA"]}
    for name, valve in all_valve_dict.items():
        if valve.rate > 0:
            useable_valves[name] = valve

    all_flows = work_through_valve_list(useable_valves)
    print(f"Part I max flow found {max(all_flows)}")

    # remove 'AA' from useable valves to allow clean generation of valve sets
    useable_valves.pop("AA")
    max_combi_flow = 0
    for r in range(1, 1 + len(useable_valves) // 2):
        my_combinations = combinations(useable_valves, r)
        for combi in my_combinations:
            valve_set1 = set(combi)
            valve_set2 = set(useable_valves).difference(valve_set1)
            useable_valves_1 = {"AA": all_valve_dict["AA"]}
            useable_valves_2 = {"AA": all_valve_dict["AA"]}
            for name in valve_set1:
                useable_valves_1[name] = useable_valves[name]
            for name in valve_set2:
                useable_valves_2[name] = useable_valves[name]
            combi_flow_1 = max(work_through_valve_list(useable_valves_1))
            combi_flow_2 = max(work_through_valve_list(useable_valves_2))
            if combi_flow_1 + combi_flow_2 > max_combi_flow:
                max_combi_flow = combi_flow_1 + combi_flow_2

    print(f"Part II output {max_combi_flow}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
