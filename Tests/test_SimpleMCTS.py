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

    def test_SimpleMCTS_nonTerminal2(self):
        state = [['X', 'O', 'O'], ['X', 'X', 6], [7, 'X', 'O']]
        value = AIPlay(state, 'O')
        self.assertEqual(value, [[2, 1], 'O'], "incorrect output from minValue")

    def test_SimpleMCTS_nonTerminal1(self):
        state = [['X', 'O', 3], [4, 'O', 6], ['X', 8, 'X']]
        value = AIPlay(state, 'O')
        self.assertEqual(value, [[1, 2], 'O'], "incorrect output from minValue")

    def test_MCR_type(self):
        state = [[['X', 'O', 3], [4, 'O', 6], ['X', 8, 'X']], 0]
        mcrValue = MCR(state)
        self.assertIs(type(mcrValue), int)

