import unittest
import pandas as pd
import pm4py
from optimiist.split_log.split_base_operator import split_base_operator

class TestSplitBaseOperator(unittest.TestCase):

  def setUp(self):
    data = {
      "case:concept:name": [1, 1, 2, 2, 3, 3],
      "concept:name": ["A", "B", "A", "C", "B", "D"]
    }
    self.log_1 = pm4py.read_xes("tests/logs/test_log_1_2_simple.xes")
    self.log = pd.DataFrame(data)

  def test_split_base_operator_simple(self):
    activities_partition_1 = ["Activity A"]
    activities_partition_2 = ["Activity B"]
    
    log_partition_1, log_partition_2, empty_cases_1, empty_cases_2 = split_base_operator(self.log_1, activities_partition_1, activities_partition_2, 100)
    
    self.assertEqual(len(log_partition_1), 1)
    self.assertEqual(len(log_partition_2), 1)
    self.assertEqual(empty_cases_1, 100)
    self.assertEqual(empty_cases_2, 100)

    # Asses correctness of the split
    self.assertEqual(log_partition_1["concept:name"].iloc[0], "Activity A")
    self.assertEqual(log_partition_2["concept:name"].iloc[0], "Activity B")

  def test_split_base_operator(self):
    activities_partition_1 = ["A", "B"]
    activities_partition_2 = ["C", "D"]
    
    log_partition_1, log_partition_2, empty_cases_1, empty_cases_2 = split_base_operator(self.log, activities_partition_1, activities_partition_2, 100)
    
    self.assertEqual(len(log_partition_1), 4)
    self.assertEqual(len(log_partition_2), 2)
    self.assertEqual(empty_cases_1, 100)
    self.assertEqual(empty_cases_2, 101)

    # Asses correctness of the split
    self.assertEqual(log_partition_1["concept:name"].iloc[0], "A")
    self.assertEqual(log_partition_1["concept:name"].iloc[1], "B")
    self.assertEqual(log_partition_1["concept:name"].iloc[2], "A")
    self.assertEqual(log_partition_1["concept:name"].iloc[3], "B")
    self.assertEqual(log_partition_2["concept:name"].iloc[0], "C")
    self.assertEqual(log_partition_2["concept:name"].iloc[1], "D")

if __name__ == '__main__':
  unittest.main()