import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src')  # gets the root directory no matter where the value

from src.SimpleMCTS import *


class SimpleMCTS(unittest.TestCase):
    def test_SimpleMCTS_block_move(self):
        state = [['X', 'O', 'X'], ['X', 'O', 'O'], [7, 'X', 9]]
        bestAction = AIPlay(state, 'O')
        expectedAction = [[0, 2], 'O']
        self.assertEqual(bestAction, expectedAction, "incorrect output from MinimaxAlphaBeta")

    def test_SimpleMCTS_right_move(self):
        state = [['O', 2, 'O'], [4, 'X', 6], ['X', 8, 9]]
        bestAction = AIPlay(state, 'O')
        expectedAction = [[1, 0], 'O']
        self.assertEqual(bestAction, expectedAction, "incorrect output from MinimaxAlphaBeta")

