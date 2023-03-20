import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src') #gets the root directory no matter where the value

from src.AI import *
from src.Initialise import *


class TestTerminalTest(unittest.TestCase):
    if board_size == 3:
        # tests a terminal X win state
        def test3x3TerminalXWinState(self):
            terminalState = [[['X', 'O', 'X'], ['O', 'X', 'O'], ['X', 8, 9]], 0]
            terminalBoolean, value, emptyState = terminalTest(terminalState)
            self.assertEqual(terminalBoolean, True, "incorrect terminalTest boolean output")
            self.assertEqual(value, -1, "incorrect terminalTest value output")
            self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")

        # tests a terminal O win state
        def test3x3TerminalOWinState(self):
            terminalState = [[['X', 'O', 'X'], ['X', 'O', 6], [7, 'O', 'X']], 1]
            terminalBoolean, value, emptyState = terminalTest(terminalState)
            self.assertEqual(terminalBoolean, True, "incorrect terminalTest boolean output")
            self.assertEqual(value, 1, "incorrect terminalTest value output")
            self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")

        # tests a draw state
        def test3x3DrawState(self):
            terminalState = [[['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']], 0]
            terminalBoolean, value, emptyState = terminalTest(terminalState)
            self.assertEqual(terminalBoolean, True, "incorrect terminalTest boolean output")
            self.assertEqual(value, 0, "incorrect terminalTest value output")
            self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")

        # tests non terminal state

        def test3x3NonTerminalState(self):
            nonTerminalState = [[['X', 2, 3], ['O', 5, 6], [7, 8, 9]], 1]
            terminalBoolean, value, emptyState = terminalTest(nonTerminalState)
            self.assertEqual(terminalBoolean, False, "incorrect terminalTest boolean output")
            self.assertEqual(value, None, "incorrect terminalTest value output")
            self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")

        def test15x15TerminalXWinState(self):
            pass
