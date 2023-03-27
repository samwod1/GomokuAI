import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src')  # gets the root directory no matter where the value

from src.MinimaxAlphaBeta import *


class TestMiniMaxAlphaBeta(unittest.TestCase):

    def TestminimaxAlphaBeta(self):
        state = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0]
        bestAction = minimaxAlphaBeta(state)
        expectedAction = [[0, 0], 'O']
        self.assertEqual(bestAction, expectedAction, "incorrect output from MinimaxAlphaBeta")

