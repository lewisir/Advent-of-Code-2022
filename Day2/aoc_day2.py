"""
--- Advent of Code 2022 ---
--- Day 2: Rock Paper Scissors ---
"""


def rps_win_lose_draw(opponent_rps, my_rps):
    """Return the points for winning, losing or drawing"""
    score_matrix = {
        "A": {"X": 3, "Y": 6, "Z": 0},
        "B": {"X": 0, "Y": 3, "Z": 6},
        "C": {"X": 6, "Y": 0, "Z": 3},
    }
    return score_matrix[opponent_rps][my_rps]


def rps_selection(opponent_rps, match_result):
    """Return the Rock, Paper or Scissors result to give the match result"""
    match_result_dict = {"X": "Lose", "Y": "Draw", "Z": "Win"}
    match_result_text = match_result_dict[match_result]
    rps_selection_matrix = {
        "Win": {"A": "Y", "B": "Z", "C": "X"},
        "Draw": {"A": "X", "B": "Y", "C": "Z"},
        "Lose": {"A": "Z", "B": "X", "C": "Y"},
    }
    return rps_selection_matrix[match_result_text][opponent_rps]


def main():
    """Main program"""
    filename = "Day2/input_day2.txt"
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))

    my_rps_scores = {"X": 1, "Y": 2, "Z": 3}

    match_scores = {"X": 0, "Y": 3, "Z": 6}

    total_score = 0
    for match in file_data:
        opponent_rps = match[0]
        my_rps = match[2]
        match_score = rps_win_lose_draw(opponent_rps, my_rps)
        total_score += match_score + my_rps_scores[my_rps]

    print(f"Part I - Total Score {total_score}")

    total_score = 0
    for match in file_data:
        opponent_rps = match[0]
        match_result = match[2]
        match_score = match_scores[match_result]
        total_score += (
            match_score + my_rps_scores[rps_selection(opponent_rps, match_result)]
        )

    print(f"Part II - Total Score {total_score}")


if __name__ == "__main__":
    main()
