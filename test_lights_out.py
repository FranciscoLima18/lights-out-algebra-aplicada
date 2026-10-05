import unittest

from lights_out import _build_adjacency_matrix, solve_lights_out


def _apply_presses(board, presses):
    size = len(board)
    result = [row[:] for row in board]
    for index, press in enumerate(presses):
        if not press:
            continue
        row, col = divmod(index, size)
        for neighbor_row, neighbor_col in (
            (row, col),
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ):
            if 0 <= neighbor_row < size and 0 <= neighbor_col < size:
                result[neighbor_row][neighbor_col] ^= 1
    return result


class LightsOutTest(unittest.TestCase):
    def test_single_cell_board(self):
        self.assertEqual(solve_lights_out([[1]]), [1])
        self.assertEqual(solve_lights_out([[0]]), [0])

    def test_three_by_three_solution_matches_board(self):
        expected_presses = [1, 0, 1, 0, 1, 0, 1, 0, 1]
        board = _apply_presses(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]], expected_presses
        )

        self.assertEqual(solve_lights_out(board), expected_presses)

    def test_adjacency_matrix_has_one_row_per_cell(self):
        matrix = _build_adjacency_matrix(2)

        self.assertEqual(len(matrix), 4)
        self.assertTrue(all(len(row) == 4 for row in matrix))
        self.assertEqual(matrix[0], [1, 1, 1, 0])

    def test_invalid_board_raises_value_error(self):
        invalid_boards = [[], [[0, 1]], [[0, 1], [1]], [[0, 2]], [[True]], "01"]
        for board in invalid_boards:
            with self.subTest(board=board):
                with self.assertRaises(ValueError):
                    solve_lights_out(board)

    def test_non_unique_system_returns_a_solution(self):
        presses = solve_lights_out([[0, 0, 0, 0]] * 4)

        self.assertEqual(len(presses), 16)
        self.assertEqual(
            _apply_presses([[0, 0, 0, 0]] * 4, presses),
            [[0] * 4 for _ in range(4)],
        )

    def test_inconsistent_system_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "no solution"):
            solve_lights_out(
                [
                    [1, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                ]
            )

    def test_solution_turns_off_three_four_and_five_by_five_boards(self):
        for size in (3, 4, 5):
            with self.subTest(size=size):
                expected_presses = [
                    (row * size + column + row + column) % 2
                    for row in range(size)
                    for column in range(size)
                ]
                initial_board = _apply_presses(
                    [[0] * size for _ in range(size)], expected_presses
                )

                presses = solve_lights_out(initial_board)
                final_board = _apply_presses(initial_board, presses)

                self.assertEqual(len(presses), size * size)
                self.assertEqual(final_board, [[0] * size for _ in range(size)])


if __name__ == "__main__":
    unittest.main()
