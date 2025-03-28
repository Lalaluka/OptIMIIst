import unittest
from pulp import LpProblem, LpVariable, LpBinary, LpMaximize, LpMinimize, value
from optimiist.optimiist_fallthrough.cut_detection.utils import extract_partitions_pulp as extract_partitions
from optimiist.optimiist_fallthrough.cut_detection.utils import get_solver


solver = get_solver()
class TestUtils(unittest.TestCase):
  def test_extract_partitions_all_ones(self):
    model = LpProblem("TestModel", LpMaximize)
    x = {}
    x['a'] = LpVariable('a', cat=LpBinary)
    x['b'] = LpVariable('b', cat=LpBinary)
    x['c'] = LpVariable('c', cat=LpBinary)

    model += x['a'] + x['b'] + x['c']
    model.solve(solver())

    partition_1, partition_2 = extract_partitions(x)
    self.assertEqual(partition_1, ['a', 'b', 'c'])
    self.assertEqual(partition_2, [])

  def test_extract_partitions_all_zeros(self):
    model = LpProblem("TestModel", LpMinimize)
    x = {}
    x['a'] = LpVariable('a', cat=LpBinary)
    x['b'] = LpVariable('b', cat=LpBinary)
    x['c'] = LpVariable('c', cat=LpBinary)

    model += x['a'] + x['b'] + x['c']
    model.solve(solver())

    partition_1, partition_2 = extract_partitions(x)
    self.assertEqual(partition_1, [])
    self.assertEqual(partition_2, ['a', 'b', 'c'])

  def test_extract_partitions_mixed(self):
    model = LpProblem("TestModel", LpMaximize)
    x = {}
    x['a'] = LpVariable('a', cat=LpBinary)
    x['b'] = LpVariable('b', cat=LpBinary)
    x['c'] = LpVariable('c', cat=LpBinary)

    model += x['a'] + x['b'] - x['c']
    model.solve(solver())

    partition_1, partition_2 = extract_partitions(x)
    self.assertEqual(partition_1, ['a', 'b'])
    self.assertEqual(partition_2, ['c'])

if __name__ == '__main__':
  unittest.main()