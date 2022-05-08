"""
file: Ripple.py
description: Solve the Ripple Effect puzzle in each file given on the command
line, first with a brute force solver, then with an intelligent solver using
the minimum-remaining-values heuristic, then compare their respective times
to run, and number of calls to their solve functions.
"""
import sys
import time
import BruteForce_Solver as BruteForce
import Intelligent_Solver_Heuristic as Heuristic


class Puzzle:
    """
    Class: Puzzle
    Description: Puzzle holds a Ripple Effect puzzle and provides methods for
                 interacting with said puzzle.
    """
    def __init__(self, width, height, puzzle, puzzle_str, regions, region_map):
        self.width = width
        self.height = height
        self.puzzle = puzzle
        self.puzzle_str = puzzle_str
        self.regions = regions
        self.region_map = region_map
        self.solved = False
        self.empty_slots_left = 0
        for row in puzzle:
            for elem in row:
                if elem == ".":
                    self.empty_slots_left += 1

    def __str__(self):
        result = ""
        walls = True
        for i in range(len(self.puzzle_str)):
            if walls:
                walls = False
                result += self.puzzle_str[i] + "\n"
            else:
                walls = True
                result += str.format(self.puzzle_str[i], self.puzzle) + "\n"
        return result

    def __repr__(self):
        return str(self)

    def get_region(self, square):
        """
        Return the region containing the given square.
        :param square: the given square
        :return: the region containing the given square,
                 or None if it does not exist
        """
        if square in self.region_map:
            return self.region_map[square]
        else:
            return None

    def __getitem__(self, row):
        return self.puzzle[row]

    def get(self, square):
        """
        Return the value at the given square within this puzzle.
        :param square: the given square
        :return: the value at the given square
        """
        return self.puzzle[square[0]][square[1]]

    def test(self, row, col, num):
        """
        Test if the given number is valid if placed at the given row and column
        within the puzzle. If it is valid, the number is placed there.
        :param row: the given row
        :param col: the given column
        :param num: the number to test placing
        :return: whether the number is valid if placed at the given row and column
        """
        temp = self.puzzle[row][col]
        self.puzzle[row][col] = num
        if self.is_valid(row, col):
            self.empty_slots_left -= 1
            return True
        else:
            self.puzzle[row][col] = temp
            return False

    def is_valid(self, row, col, check_region=True):
        """
        Check if the row at the given index and the column at the given index
        are valid. If check_region is true, check if the region containing the
        square (row, col) is valid.
        :param row: the row index
        :param col: the column index
        :param check_region: whether to check the region
        :return: whether the row, column, and region (if checked) are all valid
        """
        # check row
        prev = dict()
        for p_col in range(len(self.puzzle[row])):
            elem = self.puzzle[row][p_col]
            if type(elem) == int:
                if elem not in prev:
                    prev[elem] = [p_col]
                else:
                    for col_idx in prev[elem]:
                        if p_col - col_idx <= elem:
                            return False
                    prev[elem].append(p_col)

        # check col
        prev = dict()
        for p_row in range(len(self.puzzle)):
            elem = self.puzzle[p_row][col]
            if type(elem) == int:
                if elem not in prev:
                    prev[elem] = [p_row]
                else:
                    for row_idx in prev[elem]:
                        if p_row - row_idx <= elem:
                            return False
                    prev[elem].append(p_row)

        if not check_region:
            return True

        # check region
        region = self.get_region((row, col))
        return self.is_region_valid(region)

    def is_region_valid(self, region):
        """
        Check if the given region is valid.
        :param region: the region to check
        :return: whether region is valid
        """
        if region is None:
            return False
        else:
            seen = set()
            for square in region:
                number = self.get(square)
                if number in seen:
                    return False
                if number != ".":
                    seen.add(number)

        return True

    def is_solved(self):
        """
        Test if this puzzle has been solved.
        :return: True if the puzzle is solved, False otherwise
        """
        if self.solved:
            return True
        if self.empty_slots_left > 0:
            return False

        # check that each square is filled
        for row in range(self.height):
            for col in range(self.width):
                if self.puzzle[row][col] == ".":
                    return False

        # check each row and column
        col = 0
        for row in range(self.height):
            col = col % self.width
            if not self.is_valid(row, col, False):
                return False
            col += 1

        # check each region
        for region in self.regions:
            if not self.is_region_valid(region):
                return False

        self.solved = True
        return True

    def backtrack(self, row, col):
        """
        Backtrack by resetting the square at the given row and column to its
        default value.
        :param row: the given row
        :param col: the given column
        :return: None
        """
        self.puzzle[row][col] = "."
        self.empty_slots_left += 1

    def copy(self):
        """
        Return a deep copy of this puzzle.
        :return: a deep copy of this puzzle
        """
        puzzle_copy = [[0 for _ in range(self.width)] for __ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                puzzle_copy[row][col] = self.puzzle[row][col]
        return Puzzle(self.width, self.height, puzzle_copy, self.puzzle_str, self.regions, self.region_map)


def solve_region(row, col, width, height, puzzle, has_region):
    """
    Find all squares that make up the region the square (row, col) is in.
    :param row: the given row
    :param col: the given column
    :param width: the width of the puzzle
    :param height: the height of the puzzle
    :param puzzle: the given Ripple Effect puzzle
    :param has_region: the set of squares that are already part of a region
    :return: a tuple containing all squares that make up the region
    """
    str_row = (2 * row) + 1
    str_col = (2 * col) + 1
    has_region.add((row, col))
    new_squares = []
    # check above
    if row > 0:
        if puzzle[str_row - 1][str_col] == " ":
            new_squares.append((row - 1, col))

    # check below
    if row + 1 < height:
        if puzzle[str_row + 1][str_col] == " ":
            new_squares.append((row + 1, col))

    # check left
    if col > 0:
        if puzzle[str_row][str_col - 1] == " ":
            new_squares.append((row, col - 1))

    # check right
    if col + 1 < width:
        if puzzle[str_row][str_col + 1] == " ":
            new_squares.append((row, col + 1))

    result = [(row, col)]
    for square in new_squares:
        if square not in has_region:
            result.extend(solve_region(square[0], square[1], width, height, puzzle, has_region))

    return tuple(result)


def read_puzzle(file_name):
    """
    Read in a Ripple Effect puzzle from a file, and create a Puzzle object to
    represent it.
    :param file_name: the name of the file containing the Ripple Effect puzzle
    :return: the Puzzle object representing the Ripple Effect puzzle
    """
    # read file
    with open(file_name) as f:
        line_1 = f.readline()
        line_1 = line_1.split()
        width = int(line_1[1])
        height = int(line_1[0])
        puzzle = []

        for line in f:
            puzzle.append(line[:-1])

    # solve regions
    has_region = set()
    regions = []
    region_map = dict()
    for row in range(height):
        for col in range(width):
            if (row, col) not in has_region:
                result = solve_region(row, col, width, height, puzzle, has_region)
                regions.append(result)
                for square in result:
                    region_map[square] = result

    # create puzzle array
    puzzle_squares = [[0 for _ in range(width)] for __ in range(height)]
    for row in range(height):
        for col in range(width):
            str_row = (2 * row) + 1
            str_col = (2 * col) + 1
            if puzzle[str_row][str_col] == ".":
                puzzle_squares[row][col] = "."
            else:
                puzzle_squares[row][col] = int(puzzle[str_row][str_col])

    # create puzzle string for printing
    puzzle_str = []
    row = 0
    for line in puzzle:
        if "." not in line:
            puzzle_str.append(line)
        else:
            col = 0.0
            new_line = line[0]
            i = 1
            while i < len(line):
                if line[i] == ".":
                    new_line += "{0[" + str(row) + "][" + str(int(col)) + "]}"
                else:
                    new_line += line[i]
                i += 1
                col += .5
            puzzle_str.append(new_line)
            row += 1

    # return the created puzzle object
    return Puzzle(width, height, puzzle_squares, puzzle_str, regions, region_map)


def compare(puzzle_file, print_solved_puzzle=False):
    """
    Compare the efficiency of the brute force solver and the intelligent solver
    by looking at their respective times to run, and number of calls to their
    solve functions.
    :param puzzle_file: the puzzle file to get the Ripple Effect puzzle from
    :param print_solved_puzzle: whether the solved puzzles should be printed
    :return: None
    """
    # get the puzzle
    puzzle = read_puzzle(puzzle_file)

    # run the brute force solver
    puzzle_copy_1 = puzzle.copy()
    start = time.perf_counter()
    brute_force, brute_force_calls = BruteForce.solve(puzzle_copy_1, True)
    total = time.perf_counter() - start
    print("The Brute Force Solver took", total, "seconds to run, and called its solve function",
          brute_force_calls, "times!")
    if print_solved_puzzle:
        print(brute_force)
    print()

    # run the intelligent solver
    puzzle_copy_2 = puzzle.copy()
    start = time.perf_counter()
    heuristic, heuristic_calls = Heuristic.solve(puzzle_copy_2, True)
    total = time.perf_counter() - start
    print("The Intelligent Solver using the minimum-remaining-values heuristic took", total,
          "seconds to run, and called its solve function", heuristic_calls, "times!")
    if print_solved_puzzle:
        print(heuristic)
    print()


def main():
    """
    Ripple.py is run as:
        python Ripple.py [-prnt] puzzle_file [**more_puzzle_files]
            puzzle_file: a file containing a Ripple effect Puzzle
    :return: None
    """
    files = ["re0.txt", "re1.txt", "re10a.txt", "re10b.txt", "re18.txt"]
    test_files = ["test1.txt", "test2.txt"]
    print_solved_puzzle = False
    idx = 1
    if len(sys.argv) > 1:
        if sys.argv[1] == "-prnt":
            print_solved_puzzle = True
            idx = 2
        if sys.argv[idx] == "short":
            print("Running short tests.\n")
            target_files = test_files
        elif sys.argv[idx] == "long":
            print("Running long tests.")
            print("WARNING: The last test make take as much as 20 minutes for the brute force solver!\n")
            target_files = files
        else:
            print("running with the following files:", ", ".join(sys.argv[idx:]) )
            target_files = sys.argv[idx:]
    else:
        print("Usage: python [-prnt] Ripple.py puzzle_file [**more_puzzle_files]")
        return

    for puzzle_file in target_files:
        print("File:", puzzle_file)
        compare(puzzle_file, print_solved_puzzle)
        print()


if __name__ == '__main__':
    main()
