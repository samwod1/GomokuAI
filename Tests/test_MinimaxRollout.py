import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src')  # gets the root directory no matter where the value

from src.MinimaxRollout import *


class MinimaxRollout(unittest.TestCase):
    def test_minimax_rollout_maxDepth(self):
        state = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0]
        bestAction = minimaxRollout(state)
        expectedAction = [[0, 0], 0]
        self.assertEqual(bestAction, expectedAction, "incorrect output from MinimaxAlphaBeta")

    def test_minValue_terminal_human_win(self):
        state = [[['X', 'X', 'X'], [4, 5, 6], [7, 8, 9]], 0]
        alpha = -m.inf
        beta = m.inf
        depth = 0
        value = minValue(state, alpha, beta, depth)
        self.assertEqual(value, -1, "incorrect output from minValue")

    def test_maxValue_terminal_human_win(self):
        state = [[['X', 'X', 'X'], [4, 5, 6], [7, 8, 9]], 0]
        alpha = -m.inf
        beta = m.inf
        depth = 0
        value = minValue(state, alpha, beta, depth)
        self.assertEqual(value, -1, "incorrect output from minValue")



