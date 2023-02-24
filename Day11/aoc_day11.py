"""
--- Advent of Code 2022 ---
--- Day 11: Monkey in the Middle ---
"""


TEST = False

DAY = "11"
REAL_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2022/Day" + DAY + "/input_test.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

from time import perf_counter


class Monkey:
    """Model a Monkey with things that it throws"""

    def __init__(
        self, name, operation, divisor, true_monkey, false_monkey, ease_worry_factor=3
    ) -> None:
        self.name = name
        self.operation = operation
        self.divisor = divisor
        self.items = []
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.num_items_inspected = 0
        self.ease_worry_factor = ease_worry_factor

    def process_items(self, common_multiple=1) -> list:
        """Process the Monkey's items"""
        thrown_items = []
        for index, item in enumerate(self.items):
            updated_item = self.operate(item, common_multiple)
            self.items[index] = updated_item
            thrown_items.append((self.throw(updated_item), updated_item))
            self.num_items_inspected += 1
        self.items = []
        return thrown_items

    def operate(self, item, common_multiple):
        operator = self.operation[3]
        value = self.operation[4:]
        if value == "old":
            value = item
        else:
            value = int(value)
        if operator == "+":
            return (item + value) // self.ease_worry_factor
        elif operator == "*":
            # return (item * value) // self.ease_worry_factor
            if self.ease_worry_factor != 1:
                return (item * value) // self.ease_worry_factor
            else:
                item = item - common_multiple * (item // common_multiple)
                return item * value
        else:
            print("Unrecgonised Operator")
            return None

    def throw(self, item) -> int:
        """Test the item and return the monkey that the item is thrown to"""
        if item % self.divisor == 0:
            return self.true_monkey
        else:
            return self.false_monkey

    def catch(self, item) -> None:
        """Receive an item thrown from a Monkey (also used to add items)"""
        self.items.append(item)

    def display(self):
        """Disaply the Monkey's Items"""
        print(
            f"Monkey {self.name} inspected {self.num_items_inspected} and has {self.items}"
        )


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_input(input_data, worry_factor=3):
    """process the input data and return a dictionary of Monkeys"""
    monkeys = {}
    for data_line in input_data:
        if data_line != "":
            line = data_line.lstrip().split()
            command = line[0]
            if command == "Monkey":
                monkey_name = line[1].rstrip(":")
            elif command == "Starting":
                starting_items = line[2:]
                starting_items = [int(x.rstrip(",")) for x in starting_items]
            elif command == "Operation:":
                operation = "".join(line[3:])
            elif command == "Test:":
                divisor = int(line[3])
            elif command == "If":
                if line[1] == "true:":
                    true_monkey = line[5]
                elif line[1] == "false:":
                    false_monkey = line[5]
        elif data_line == "":  # Input needs to end in two blank lines!
            monkeys[monkey_name] = Monkey(
                monkey_name, operation, divisor, true_monkey, false_monkey, worry_factor
            )
            for item in starting_items:
                monkeys[monkey_name].catch(item)
    return monkeys


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    my_monkeys = process_input(input_data)
    for _ in range(20):
        for monkey in my_monkeys.values():
            thrown_items = monkey.process_items()
            for to_monkey in thrown_items:
                my_monkeys[to_monkey[0]].catch(to_monkey[1])

    inspected_item_count = []
    for monkey in my_monkeys.values():
        inspected_item_count.append(monkey.num_items_inspected)

    inspected_item_count.sort(reverse=True)
    monkey_business = inspected_item_count[0] * inspected_item_count[1]

    print(f"Part I - Monkey Business {monkey_business}")

    my_monkeys = process_input(input_data, 1)
    common_multiple = 1
    for monkey in my_monkeys.values():
        common_multiple *= monkey.divisor
    print(f"Common Multiple {common_multiple}")
    for _ in range(10000):
        for monkey in my_monkeys.values():
            thrown_items = monkey.process_items(common_multiple)
            for to_monkey in thrown_items:
                my_monkeys[to_monkey[0]].catch(to_monkey[1])

    inspected_item_count = []
    for monkey in my_monkeys.values():
        inspected_item_count.append(monkey.num_items_inspected)

    inspected_item_count.sort(reverse=True)
    monkey_business = inspected_item_count[0] * inspected_item_count[1]

    print(f"Part II - Monkey Business {monkey_business}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
