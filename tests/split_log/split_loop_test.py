import unittest
import pandas as pd
from optimiist.split_log.split_loop import split_loop

class TestSplitLoop(unittest.TestCase):

  def setUp(self):
    data = {
      "case:concept:name": [1, 1, 1, 2, 3, 3],
      "concept:name": ["A", "B", "A", "C", "B", "D"]
    }
    self.log = pd.DataFrame(data)

  def test_split_loop_simple(self):
    activities_partition_1 = ["A", "C", "D"]
    activities_partition_2 = ["B"]
    empty_cases = 0

    log_partition_1, log_partition_2, empty_cases_1, empty_cases_2 = split_loop(self.log, activities_partition_1, activities_partition_2, empty_cases)

    self.assertEqual(len(log_partition_1), 4)
    self.assertEqual(len(log_partition_2), 2)
    self.assertEqual(empty_cases_1, 1)
    self.assertEqual(empty_cases_2, 0)

    self.assertEqual(log_partition_1["concept:name"].iloc[0], "A")
    self.assertEqual(log_partition_1["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(log_partition_1["concept:name"].iloc[1], "A")
    self.assertEqual(log_partition_1["case:concept:name"].iloc[1], "1🚫️SPLIT_1")
    self.assertEqual(log_partition_1["concept:name"].iloc[2], "C")
    self.assertEqual(log_partition_1["case:concept:name"].iloc[2], "2🚫️SPLIT_0")
    self.assertEqual(log_partition_1["concept:name"].iloc[3], "D")
    self.assertEqual(log_partition_1["case:concept:name"].iloc[3], "3🚫️SPLIT_1")
    self.assertEqual(log_partition_2["concept:name"].iloc[0], "B")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(log_partition_2["concept:name"].iloc[1], "B")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[1], "3🚫️SPLIT_0")

  def test_split_loop_complex(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 1, 2, 2, 2],
      "concept:name": ["A", "B", "C", "A", "C", "A"]
    })
    activities_partition_1 = ["B"]
    activities_partition_2 = ["A", "C"]

    log_partition_1, log_partition_2, empty_cases_1, empty_cases_2 = split_loop(log, activities_partition_1, activities_partition_2, 0)

    self.assertEqual(len(log_partition_1), 1)
    self.assertEqual(len(log_partition_2), 5)

    self.assertEqual(empty_cases_1, 4)
    self.assertEqual(empty_cases_2, 0)

    self.assertEqual(log_partition_1["concept:name"].iloc[0], "B")
    self.assertEqual(log_partition_1["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(log_partition_2["concept:name"].iloc[0], "A")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(log_partition_2["concept:name"].iloc[1], "C")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
    self.assertEqual(log_partition_2["concept:name"].iloc[2], "A")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[2], "2🚫️SPLIT_0")
    self.assertEqual(log_partition_2["concept:name"].iloc[3], "C")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[3], "2🚫️SPLIT_0")
    self.assertEqual(log_partition_2["concept:name"].iloc[4], "A")
    self.assertEqual(log_partition_2["case:concept:name"].iloc[4], "2🚫️SPLIT_0")

  def test_split_case_in_loop(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 1, 2, 2, 2],
      "concept:name": ["A", "B", "C", "A", "C", "A"]
    })
    activities_partition_1 = []
    activities_partition_2 = ["B", "A", "C"]

    log_partition_1, log_partition_2, empty_cases_1, empty_cases_2 = split_loop(log, activities_partition_1, activities_partition_2, 0)

    self.assertEqual(len(log_partition_1), 0)
    self.assertEqual(len(log_partition_2), 6)

    self.assertEqual(empty_cases_1, 4)
    self.assertEqual(empty_cases_2, 0)

if __name__ == '__main__':
  unittest.main()