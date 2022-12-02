"""
--- Advent of Code 2022 ---
--- Day 2: Rock Paper Scissors ---
"""


def rsp_win_lose_draw(oppent_rps, my_rps):
    """Return the points for winning, losing or drawing"""
    score_matrix = {
        "A": {"X": 3, "Y": 6, "Z": 0},
        "B": {"X": 0, "Y": 3, "Z": 6},
        "C": {"X": 6, "Y": 0, "Z": 3},
    }
    return score_matrix[oppent_rps][my_rps]


def main():
    """Main program"""
    filename = "Day2/input_day2.txt"
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))

    opponent_rps_scores = {"A": 1, "B": 2, "C": 3}

    my_rps_scores = {"X": 1, "Y": 2, "Z": 3}

    total_score = 0

    for match in file_data:
        opponent_rps = match[0]
        my_rps = match[2]
        match_score = rsp_win_lose_draw(opponent_rps, my_rps)
        total_score += match_score + my_rps_scores[my_rps]

    print(f"Part I - Total SCore {total_score}")


if __name__ == "__main__":
    main()
