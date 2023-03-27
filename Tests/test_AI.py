import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + '/src')  # gets the root directory no matter where the project

from src.AI import *


class TestTerminalTest(unittest.TestCase):
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

    def test15x15TerminalXWinState(self):  # win condition is still 3, usually would be higher on bigger boards
        count = 0
        terminalBoard = []
        for i in range(15):
            count += 1
            terminalBoard.append([count])
            for j in range(15 - 1):
                count += 1
                terminalBoard[i].append(count)

        # insert moves into the board
        terminalState = [terminalBoard, 'O']
        terminalState[0][0][0] = 'X'
        terminalState[0][0][1] = 'X'
        terminalState[0][0][2] = 'X'

        terminalBoolean, value, emptyState = terminalTest(terminalState)
        self.assertEqual(terminalBoolean, True, "incorrect terminalTest boolean output")
        self.assertEqual(value, -1, "incorrect terminalTest value output")
        self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")

    def test15x15TerminalOWinState(self):  # win condition is still 3, usually would be higher on bigger boards
        count = 0
        terminalBoard = []
        for i in range(15):
            count += 1
            terminalBoard.append([count])
            for j in range(15 - 1):
                count += 1
                terminalBoard[i].append(count)

        # insert moves into the board
        terminalState = [terminalBoard, 'O']
        terminalState[0][0][0] = 'O'
        terminalState[0][1][0] = 'O'
        terminalState[0][2][0] = 'O'

        terminalBoolean, value, emptyState = terminalTest(terminalState)
        self.assertEqual(terminalBoolean, True, "incorrect terminalTest boolean output")
        self.assertEqual(value, 1, "incorrect terminalTest value output")
        self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")

    def test15x15NonTerminalState(self):  # win condition is still 3, usually would be higher on bigger boards
        count = 0
        terminalBoard = []
        for i in range(15):
            count += 1
            terminalBoard.append([count])
            for j in range(15 - 1):
                count += 1
                terminalBoard[i].append(count)

        # insert moves into the board
        terminalState = [terminalBoard, 'O']

        terminalBoolean, value, emptyState = terminalTest(terminalState)
        self.assertEqual(terminalBoolean, False, "incorrect terminalTest boolean output")
        self.assertEqual(value, None, "incorrect terminalTest value output")
        self.assertEqual(emptyState, [], "incorrect terminalTest empty state output")


class TestSuccessors(unittest.TestCase):

    def testSuccessors(self):
        state = [[['X', 'O', 'X'], [4, 5, 6], ['X', 'O', 'O']], 0]
        succ = successors(state)
        expectedSuccessors = [[[['X', 'O', 'X'], ['O', 5, 6], ['X', 'O', 'O']], 1],
                              [[['X', 'O', 'X'], [4, 'O', 6], ['X', 'O', 'O']], 1],
                              [[['X', 'O', 'X'], [4, 5, 'O'], ['X', 'O', 'O']], 1]]
        self.assertEqual(succ, expectedSuccessors, "incorrect output for successors")


class TestResult(unittest.TestCase):

    def testOResult(self):
        state = [[['X', 'O', 'X'], [4, 5, 6], ['X', 'O', 'O']], 'O']
        action = [[0, 1], 'O']
        r = result(state, action)
        expectedResult = [[['X', 'O', 'X'], ['O', 5, 6], ['X', 'O', 'O']], 'X']
        self.assertEqual(r, expectedResult, "incorrect output for result")

    def testXResult(self):
        state = [[['X', 'O', 'X'], [4, 5, 6], ['X', 'O', 'O']], 'X']
        action = [[0, 1], 'X']
        r = result(state, action)
        expectedResult = [[['X', 'O', 'X'], ['X', 5, 6], ['X', 'O', 'O']], 'O']
        self.assertEqual(r, expectedResult, "incorrect output for result")


class TestGetAction(unittest.TestCase):

    def testGetActions3x3(self):
        state = [[['X', 'O', 'X'], [4, 5, 6], ['X', 'O', 'O']], 'X']
        actions = getActions(state)
        expectedActions = [[[0, 1], 'X'], [[1, 1], 'X'], [[2, 1], 'X']]
        self.assertEqual(actions, expectedActions, "incorrect output for getActions")


class TestRollout(unittest.TestCase):

    def testTerminalRollout(self):
        state = [[['X', 'O', 'X'], [4, 5, 6], ['O', 'O', 'O']], 'O']
        rolloutValue = rollout(state)
        expectedValue = 1
        self.assertEqual(rolloutValue, expectedValue, "incorrect output for rollout")


class TestStateToAction(unittest.TestCase):

    def testStateToAction(self):
        initState = [['X', 'O', 'X'], [4, 5, 6], ['O', 'X', 'O']]
        bestState = [[['X', 'O', 'X'], ['O', 5, 6], ['O', 'X', 'O']], 1]

        action = stateToAction(initState, bestState)
        expectedAction = [[0, 1], 'O']
        self.assertEqual(action, expectedAction, "incorrect output for stateToAction")


class TestStateConversion(unittest.TestCase):

    def testStateConversion(self):
        board = [['X', 'O', 'X'], [4, 5, 6], ['O', 'X', 'O']]
        toMove = 'X'
        state = stateConversion(board, toMove)
        expectedState = [[['X', 'O', 'X'], [4, 5, 6], ['O', 'X', 'O']], 1]
        self.assertEqual(state, expectedState, "incorrect output for stateToAction")
