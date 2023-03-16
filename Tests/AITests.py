import unittest
import AI

class TestTerminalTest(unittest.TestCase):

  def testTerminalState(self):
    terminalState = [[['X', 'O', 'X'], ]]
    #terminalBoolean, value, path = None

  def test_normal_case(self):
    self.rectangle.set_width(2)
    self.rectangle.set_height(3)
    self.assertEqual(self.rectangle.get_area(), 6, "incorrect area")

  def test_geq(self):
    """tests if value is greater than or equal to a particular target"""
    self.assertGreaterEqual(self.rectangle.get_area(), -1)

  def test_assert_raises(self): 
    """using assertRaises to detect if an expected error is raised when running a particular block of code"""
    with self.assertRaises(ZeroDivisionError):
      a = 1 / 0