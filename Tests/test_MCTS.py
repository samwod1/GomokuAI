import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src')  # gets the root directory no matter where the value

from src.MCTS import *


class MCTS(unittest.TestCase):

    def test_functions_type(self):
        state = [['X', 'O', 'X'], ['X', 'O', 'O'], [7, 'X', 9]]

        action = AI_play(state, 'O')
        self.assertIs(type(action), list)

        node = [[['X', 'O', 'X'], ['X', 'O', 'O'], [7, 'X', 9]], 0]
        checkLeafResult = checkLeaf(node)
        self.assertIs(type(checkLeafResult), bool)

        tree.clear()
        tree[str(('[]', 'start'))] = ['start', 0, 0]
        tree[str((node, '[]'))] = [('[]', 'start'), 0, 0]

        UCB = calcMaxUCB((node, '[]'))
        self.assertIs(type(UCB), float)

    def test_MCTS_block_move(self):
        state = [['X', 'O', 'X'], ['X', 'O', 'O'], [7, 'X', 9]]
        action = AI_play(state, 'O')
        self.assertEqual(action, [[0, 2], 'O'])

    def test_MCTS_win_move(self):
        state = [['X', 2, 3], ['O', 'O', 'X'], ['X', 'O', 'X']]
        action = AI_play(state, 'O')
        self.assertEqual(action, [[1, 0], 'O'])

