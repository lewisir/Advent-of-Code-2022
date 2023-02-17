"""
--- Advent of Code 2022 ---
--- Day 13: Distress Signal ---
https://adventofcode.com/2022/day/13
"""
TEST = False

DAY = "13"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


class Packet:
    """Model a packet which is a list of intergers and/or lists"""

    def __init__(self) -> None:
        """Initialise the packet from the input string"""
        self.packet = []
        self.length = 1

    def build_packet(self, input_string, pointer=1):
        """Build the packet which is formed of lists of integers from the input string"""
        while pointer < len(input_string):
            char = input_string[pointer]
            if char == "[":
                self.packet.append(Packet())
                self.packet[-1].build_packet(input_string, pointer + 1)
                pointer += self.packet[-1].length
                self.length += self.packet[-1].length
            elif char in "]":
                pointer += 1
                self.length += 1
                break
            elif char == ",":
                pointer += 1
                self.length += 1
            elif char.isnumeric():
                result = self.get_number(input_string, pointer)
                self.packet.append(result[0])
                pointer = result[1]
                self.length += len(str(self.packet[-1]))
            else:
                print("Unrecognised content in input string")
                break

    def get_number(self, input_string, pointer):
        """Extract the integer from a string"""
        number = ""
        while input_string[pointer].isnumeric():
            number += input_string[pointer]
            pointer += 1
        return [int(number), pointer]

    def display(self):
        """Build and return a string that displays the packet"""
        display_string = ""
        for packet in self.packet:
            if isinstance(packet, Packet):
                display_string += "[" + packet.display() + ","
            else:
                display_string += str(packet) + ","
        return display_string

    def displayII(self):
        """Display the packet"""
        print(self.packet)
        for packet in self.packet:
            if isinstance(packet, Packet):
                packet.displayII()


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def compare(packet_left, packet_right):
    """Comapre two packets and return true if they're in the right order and false if not"""
    packet_len_check = None
    if len(packet_left.packet) < len(packet_right.packet):
        packet_len_check = True
    elif len(packet_left.packet) > len(packet_right.packet):
        packet_len_check = False
    for (left_packet, right_packet) in zip(
        enumerate(packet_left.packet), enumerate(packet_right.packet)
    ):
        left_index, left = left_packet
        right_index, right = right_packet
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
        elif isinstance(left, Packet) and isinstance(right, Packet):
            result = compare(left, right)
            if result is None:
                pass
            elif result:
                return True
            elif not result:
                return False
        elif isinstance(left, int) and isinstance(right, Packet):
            new_string = "[" + str(left) + "]"
            new_packet = Packet()
            new_packet.build_packet(new_string)
            result = compare(new_packet, right)
            if result is None:
                pass
            elif result:
                return True
            elif not result:
                return False
        elif isinstance(left, Packet) and isinstance(right, int):
            new_string = "[" + str(right) + "]"
            new_packet = Packet()
            new_packet.build_packet(new_string)
            result = compare(left, new_packet)
            if result is None:
                pass
            elif result:
                return True
            elif not result:
                return False
    return packet_len_check


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    packet_1 = None
    packet_2 = None
    packet_list_1 = {}
    packet_list_2 = {}
    packet_pair_count = 0
    for packet in input_data:
        if packet_1 is None:
            packet_pair_count += 1
            packet_1 = Packet()
            packet_list_1[packet_pair_count] = packet_1
            packet_list_1[packet_pair_count].build_packet(packet)
        elif packet_2 is None:
            packet_2 = Packet()
            packet_list_2[packet_pair_count] = packet_2
            packet_list_2[packet_pair_count].build_packet(packet)
        elif packet == "":
            packet_1, packet_2 = None, None

    true_packet_order_count = 0
    for packet in packet_list_1:
        result = compare(packet_list_1[packet], packet_list_2[packet])
        if result:
            true_packet_order_count += packet
    print(f"Part I - sum of correctly order packets {true_packet_order_count}")

    combined_packet_list = []
    for packet in packet_list_1.values():
        combined_packet_list.append(packet)
    for packet in packet_list_2.values():
        combined_packet_list.append(packet)

    divider_packet_1 = Packet()
    divider_packet_1.build_packet("[[2]]")
    divider_packet_2 = Packet()
    divider_packet_2.build_packet("[[6]]")

    combined_packet_list.append(divider_packet_1)
    combined_packet_list.append(divider_packet_2)

    # sort the packet list
    for packet in range(len(combined_packet_list) - 1, 0, -1):
        for index in range(packet):
            if not compare(
                combined_packet_list[index], combined_packet_list[index + 1]
            ):
                temp = combined_packet_list[index]
                combined_packet_list[index] = combined_packet_list[index + 1]
                combined_packet_list[index + 1] = temp

    position_count = 0
    for packet in combined_packet_list:
        position_count += 1
        if packet == divider_packet_1:
            divider_1 = position_count
        elif packet == divider_packet_2:
            divider_2 = position_count

    print(
        f"Divider packet 1 at {divider_1} and divider packet 2 at {divider_2} give prodyct {divider_1*divider_2}"
    )


if __name__ == "__main__":
    main()
