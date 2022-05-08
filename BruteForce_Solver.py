"""
file: BruteForce_Solver.py
description: Solve a Ripple Effect puzzle using a simple brute force solver.
"""


def solve(puzzle, count_calls=False):
    """
    Call solve_rec() to solve the given puzzle, keeping track of the number
    of times solve_rec() is called. Then, if the puzzle has been solved,
    return the solved puzzle, otherwise return None. If count_calls is true,
    also return the number of calls to solve_rec().
    :param puzzle: the Ripple Effect puzzle to solve
    :param count_calls: whether to return the number of calls to solve_rec()
    :return: the solved puzzle if it is possible, None otherwise
             if count_calls == true, also return the number of calls to solve_rec()
    """
    # solve the puzzle
    calls = [0]
    result = solve_rec(puzzle, 0, 0, calls)
    if not result.is_solved:
        result = None
    if count_calls:
        return result, calls[0]
    else:
        return result


def solve_rec(puzzle, row, col, calls):
    """
    Solve the given Ripple Effect puzzle using brute force depth first search,
    start from the top left corner of the puzzle.
    :param puzzle: the Ripple Effect puzzle being solved
    :param row: the current row
    :param col: the current column
    :param calls: the number of times solve_rec() has been called
    :return: The solved Ripple Effect puzzle
    """
    calls[0] += 1
    if puzzle.is_solved():
        return puzzle

    if col >= puzzle.width:
        col = 0
        row += 1

    if row >= puzzle.height:
        if puzzle.is_solved():
            return puzzle

    if puzzle[row][col] != ".":
        return solve_rec(puzzle, row, col + 1, calls)
    else:
        num = 0
        max_num = len(puzzle.get_region((row, col)))
        while num < max_num:
            num += 1
            if puzzle.test(row, col, num):
                solve_rec(puzzle, row, col + 1, calls)
            if puzzle.is_solved():
                return puzzle
        puzzle.backtrack(row, col)

    return puzzle
