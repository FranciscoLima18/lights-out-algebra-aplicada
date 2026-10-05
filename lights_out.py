"""Solver for the binary Lights Out puzzle."""

from collections.abc import Sequence


def _validate_board(board: Sequence[Sequence[int]]) -> list[list[int]]:
    """Validate and copy a square binary board."""
    if isinstance(board, (str, bytes)):
        raise ValueError("board must be a non-empty square matrix")

    try:
        rows = [list(row) for row in board]
    except TypeError as exc:
        raise ValueError("board must be a non-empty square matrix") from exc

    size = len(rows)
    if size == 0 or any(len(row) != size for row in rows):
        raise ValueError("board must be a non-empty square matrix")
    if any(
        isinstance(value, bool)
        or value not in (0, 1)
        or not isinstance(value, int)
        for row in rows
        for value in row
    ):
        raise ValueError("board entries must be integers equal to 0 or 1")
    return rows


def _build_adjacency_matrix(size: int) -> list[list[int]]:
    """Build the Lights Out matrix in row-major cell order."""
    cell_count = size * size
    matrix = [[0] * cell_count for _ in range(cell_count)]

    for row in range(size):
        for col in range(size):
            equation = row * size + col
            for neighbor_row, neighbor_col in (
                (row, col),
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ):
                if 0 <= neighbor_row < size and 0 <= neighbor_col < size:
                    press = neighbor_row * size + neighbor_col
                    matrix[equation][press] = 1
    return matrix


def _solve_mod2(matrix: list[list[int]], vector: list[int]) -> list[int]:
    """Solve a square binary system with XOR Gaussian elimination."""
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    variable_count = len(vector)
    rank = 0

    for column in range(variable_count):
        pivot = next(
            (row for row in range(rank, variable_count) if augmented[row][column]),
            None,
        )
        if pivot is None:
            continue

        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        for row in range(variable_count):
            if row != rank and augmented[row][column]:
                for index in range(column, variable_count + 1):
                    augmented[row][index] ^= augmented[rank][index]
        rank += 1

    if any(
        not any(row[:variable_count]) and row[variable_count]
        for row in augmented
    ):
        raise ValueError("the Lights Out system has no solution")
    solution = [0] * variable_count
    for row in augmented:
        pivot_column = next(
            (column for column, value in enumerate(row[:variable_count]) if value),
            None,
        )
        if pivot_column is not None:
            solution[pivot_column] = row[variable_count]
    return solution


def solve_lights_out(board: Sequence[Sequence[int]]) -> list[int]:
    """Return a binary press vector that solves ``board`` modulo 2.

    Cells and presses are flattened in row-major order. Pressing a cell toggles
    that cell and each orthogonal neighbor within the board. If multiple
    solutions exist, free variables are set to zero.
    """
    validated_board = _validate_board(board)
    size = len(validated_board)
    matrix = _build_adjacency_matrix(size)
    vector = [value for row in validated_board for value in row]
    return _solve_mod2(matrix, vector)
