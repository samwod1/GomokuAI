import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src')  # gets the root directory no matter where the value

from src.MinimaxAlphaBeta import *


class MinimaxAlphaBeta(unittest.TestCase):
    def test_minimax_alpha_beta(self):
        state = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0]
        bestAction = minimaxAlphaBeta(state)
        expectedAction = [[0, 0], 0]
        self.assertEqual(bestAction, expectedAction, "incorrect output from MinimaxAlphaBeta")

    def test_minValue_terminal_human_win(self):
        state = [[['X', 'X', 'X'], [4, 5, 6], [7, 8, 9]], 0]
        alpha = -m.inf
        beta = m.inf
        value = minValue(state, alpha, beta)
        self.assertEqual(value, -1, "incorrect output from minValue")

    def test_maxValue_terminal_human_win(self):
        state = [[['X', 'X', 'X'], [4, 5, 6], [7, 8, 9]], 0]
        alpha = -m.inf
        beta = m.inf
        value = maxValue(state, alpha, beta)
        self.assertEqual(value, -1, "incorrect output from minValue")

    def test_maxValue_nonTerminal(self):
        state = [[['X', 'O', 'O'], ['X', 'X', 6], [7, 'X', 'O']], 0]
        alpha = -m.inf
        beta = m.inf
        value = maxValue(state, alpha, beta)
        self.assertEqual(value, 1, "incorrect output from minValue")

    def test_minValue_nonTerminal(self):
        state = [[['X', 'O', 'O'], ['X', 'X', 6], [7, 'X', 'O']], 0]
        alpha = -m.inf
        beta = m.inf
        value = maxValue(state, alpha, beta)
        self.assertEqual(value, 1, "incorrect output from minValue")