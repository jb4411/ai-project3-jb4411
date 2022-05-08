"""
file: Intelligent_Solver_Heuristic.py
description: Solve a Ripple Effect puzzle with an intelligent solver using
the minimum-remaining-values heuristic.
"""


def solve(puzzle, count_calls=False):
    """
    Start by finding the remaining possible values for each square in the
    puzzle. Then, call solve_rec() to solve the given puzzle, passing the
    array of remaining possible values for each square to solve_rec(), and
    keeping track of the number of times solve_rec() is called. Then, if
    the puzzle has been solved, return the solved puzzle, otherwise return
    None. If count_calls is true, also return the number of calls to
    solve_rec().
    :param puzzle: the Ripple Effect puzzle to solve
    :param count_calls: whether to return the number of calls to solve_rec()
    :return: the solved puzzle if it is possible, None otherwise
             if count_calls == true, also return the number of calls to solve_rec()
    """
    rows = dict()
    cols = dict()
    regions = dict()
    remaining_dict = dict()

    # initialize cols dictionary
    for col in range(puzzle.width):
        cols[col] = set()

    # fill the rows dictionary and cols dictionary
    for row in range(puzzle.height):
        rows[row] = set()
        for col in range(puzzle.width):
            num = puzzle[row][col]
            if type(num) == int:
                rows[row].add(num)
                cols[col].add(num)

    # get the numbers in each region
    for region in puzzle.regions:
        regions[region] = set()
        for square in region:
            num = puzzle.get(square)
            if type(num) == int:
                regions[region].add(num)

    # get the range of possible values for each square
    for region in regions:
        possible = set(range(1, len(region) + 1))
        for num in regions[region]:
            possible.remove(num)

        for square in region:
            if puzzle.get(square) == ".":
                remaining_dict[square] = set(possible)
            else:
                remaining_dict[square] = puzzle.get(square)

    # reduce remaining possible values
    row_squares = []
    col_squares = []
    for row in range(puzzle.height):
        for col in range(puzzle.width):
            num = puzzle[row][col]
            if type(num) == int:
                # check row
                row_squares.append([(row, x) for x in range(puzzle.width)])
                for square in row_squares[-1]:
                    if type(remaining_dict[square]) != int:
                        if abs(square[1] - col) <= num:
                            remaining_dict[square].discard(num)

                # check col
                col_squares.append([(x, col) for x in range(puzzle.height)])
                for square in col_squares[-1]:
                    if type(remaining_dict[square]) != int:
                        if abs(square[0] - row) <= num:
                            remaining_dict[square].discard(num)

    # create array of squares to solve
    remaining = [[square, remaining_dict[square]] for square in remaining_dict if type(remaining_dict[square]) != int]
    remaining = sorted(remaining, key=lambda l: (len(l[1]), l[0], l))

    # solve the puzzle
    calls = [0]
    result = solve_rec(puzzle, remaining, calls)
    if not result.is_solved:
        result = None
    if count_calls:
        return result, calls[0]
    else:
        return result


def update_remaining(remaining, row, col, value, puzzle):
    """
    Update the array of remaining possible values for each square and sort it
    by number of remaining possible values.
    :param remaining: the array of remaining possible values for each square
    :param row: the row of the last value added
    :param col: the column of the last value added
    :param value: the last value added
    :param puzzle: the Ripple Effect puzzle being solved
    :return: the new array of remaining possible values for each square
    """
    region_squares = set(puzzle.get_region((row, col)))
    new_remaining = []
    for elem in remaining:
        temp = set(elem[1])
        # check row
        if elem[0][0] == row:
            dif = abs(col - elem[0][1])
            if dif <= value:
                temp.discard(value)
        # check col
        if elem[0][1] == col:
            dif = abs(row - elem[0][0])
            if dif <= value:
                temp.discard(value)

        # check region
        if elem[0] in region_squares:
            temp.discard(value)

        new_remaining.append([elem[0], temp])

    return sorted(new_remaining, key=lambda l: (len(l[1]), l[0], l))


def solve_rec(puzzle, remaining, calls):
    """
    Solve the given Ripple Effect puzzle using depth first search, picking the
    next target square using the minimum-remaining-values heuristic.
    :param puzzle: the Ripple Effect puzzle being solved
    :param remaining: the array of remaining possible values for each square
    :param calls: the number of times solve_rec() has been called
    :return: The solved Ripple Effect puzzle
    """
    calls[0] += 1
    if puzzle.is_solved():
        return puzzle

    current = remaining[0]
    row = current[0][0]
    col = current[0][1]
    for num in current[1]:
        if puzzle.test(row, col, num):
            new_remaining = update_remaining(remaining[1:], row, col, num, puzzle)
            solve_rec(puzzle, new_remaining, calls)
        if puzzle.is_solved():
            return puzzle
    puzzle.backtrack(row, col)

    return puzzle
