import unittest
import pandas as pd
from optimiist.split_log.split_tau_loop import split_case_in_tau_loop, split_tau_loop
import pm4py

class TestSplitTauLoop(unittest.TestCase):

  def setUp(self):
    self.start = pd.Series({"A": 1, "B": 1})
    self.end = pd.Series({"C": 1, "D": 1})

  def test_split_case_in_tau_loop_single_event(self):
    case_df = pd.DataFrame({
      "case:concept:name": [1],
      "concept:name": ["A"]
    })
    result = split_case_in_tau_loop(case_df, self.start, self.end)
    self.assertEqual(result.shape[0], 1)
    self.assertEqual(result["case:concept:name"].iloc[0], 1)

  def test_split_case_in_tau_loop_simple(self):
    case_df = pd.DataFrame({
      "case:concept:name": [1, 1, 1, 1, 1, 1],
      "concept:name": ["A", "B", "C", "A", "D", "B"]
    })
    result = split_case_in_tau_loop(case_df, self.start, self.end)

    self.assertEqual(result.shape[0], 6)
    self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[3], "1🚫️SPLIT_1")
    self.assertEqual(result["case:concept:name"].iloc[4], "1🚫️SPLIT_1")
    self.assertEqual(result["case:concept:name"].iloc[5], "1🚫️SPLIT_2")

  def test_split_case_in_tau_loop_activity_start_and_end_v1(self):
    start = pd.Series({"A": 1, "B": 1, "C": 1})
    end = pd.Series({"B": 1, "C": 1})
    case_df = pd.DataFrame({
      "case:concept:name": [1, 1, 1],
      "concept:name": ["A", "B", "C"]
    })
    result = split_case_in_tau_loop(case_df, start, end)

    self.assertEqual(result.shape[0], 3)
    self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_1")

  def test_split_case_in_tau_loop_activity_start_and_end_v2(self):
    start = pd.Series({"A": 1, "B": 1, "C": 1})
    end = pd.Series({"B": 1, "C": 1})
    case_df = pd.DataFrame({
      "case:concept:name": [1, 1, 1, 1, 1],
      "concept:name": ["A", "B", "B", "B", "C"]
    })
    result = split_case_in_tau_loop(case_df, start, end)

    self.assertEqual(result.shape[0], 5)
    self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_1")
    self.assertEqual(result["case:concept:name"].iloc[3], "1🚫️SPLIT_2")
    self.assertEqual(result["case:concept:name"].iloc[4], "1🚫️SPLIT_3")

  def test_split_case_in_tau_loop_activity_start_and_end_v3(self):
    start = pd.Series({"A": 1, "B": 1, "C": 1})
    end = pd.Series({"B": 1, "D": 1})
    case_df = pd.DataFrame({
      "case:concept:name": [1, 1, 1, 1, 1, 1],
      "concept:name": ["A", "B", "B", "B", "C", "D"]
    })
    result = split_case_in_tau_loop(case_df, start, end)

    self.assertEqual(result.shape[0], 6)
    self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_1")
    self.assertEqual(result["case:concept:name"].iloc[3], "1🚫️SPLIT_2")
    self.assertEqual(result["case:concept:name"].iloc[4], "1🚫️SPLIT_3")
    self.assertEqual(result["case:concept:name"].iloc[5], "1🚫️SPLIT_3")

  def test_split_case_in_tau_loop_activity_start_and_end_first_and_second_place(self):
    start = pd.Series({"A": 1, "B": 1})
    end = pd.Series({"B": 1, "A": 1})
    case_df = pd.DataFrame({
      "case:concept:name": [1, 1],
      "concept:name": ["A", "B"]
    })
    result = split_case_in_tau_loop(case_df, start, end)

    self.assertEqual(result.shape[0], 2)
    self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_1")

  def test_split_tau_loop_single_event(self):
      log = pd.DataFrame({
        "case:concept:name": [1],
        "concept:name": ["A"]
      })
      result, log_partition_2, empty_cases_1, empty_cases_2 = split_tau_loop(log, 0)
      self.assertEqual(result.shape[0], 1)
      self.assertEqual(result["case:concept:name"].iloc[0], 1)
      self.assertEqual(log_partition_2.shape[0], 0)
      self.assertEqual(empty_cases_1, 0)
      self.assertEqual(empty_cases_2, 0)

  def test_split_tau_loop_simple(self):
      log = pd.DataFrame({
        "case:concept:name": [1, 1, 1, 2, 2, 2],
        "concept:name": ["A", "B", "C", "A", "C", "A"]
      })
      result, log_partition_2, empty_cases_1, empty_cases_2 = split_tau_loop(log, 0)

      self.assertEqual(result.shape[0], 6)
      self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[3], "2🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[4], "2🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[5], "2🚫️SPLIT_1")
      self.assertEqual(log_partition_2.shape[0], 0)
      self.assertEqual(empty_cases_1, 0)
      self.assertEqual(empty_cases_2, 0)

  def test_split_tau_loop_with_empty_cases(self):
      log = pd.DataFrame({
        "case:concept:name": [1, 1, 1, 1, 1, 1],
        "concept:name": ["A", "B", "C", "A", "D", "B"]
      })
      result, log_partition_2, empty_cases_1, empty_cases_2 = split_tau_loop(log, 2)
      self.assertEqual(result.shape[0], 6)
      self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[3], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[4], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[5], "1🚫️SPLIT_0")
      self.assertEqual(log_partition_2.shape[0], 0)
      self.assertEqual(empty_cases_1, 2)
      self.assertEqual(empty_cases_2, 0)

  def test_split_tau_loop_multiple_cases_no_splits(self):
      log = pd.DataFrame({
        "case:concept:name": [1, 1, 1, 2, 2, 2],
        "concept:name": ["A", "B", "C", "A", "D", "B"]
      })
      result, log_partition_2, empty_cases_1, empty_cases_2 = split_tau_loop(log, 0)
      self.assertEqual(result.shape[0], 6)
      self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[3], "2🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[4], "2🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[5], "2🚫️SPLIT_0")
      self.assertEqual(log_partition_2.shape[0], 0)
      self.assertEqual(empty_cases_1, 0)
      self.assertEqual(empty_cases_2, 0)
    
  def test_split_tau_loop_multiple_cases(self):
      log = pd.DataFrame({
        "case:concept:name": [1, 1, 1, 2, 2, 2],
        "concept:name": ["A", "B", "C", "A", "D", "B"]
      })
      result, log_partition_2, empty_cases_1, empty_cases_2 = split_tau_loop(log, 0)
      self.assertEqual(result.shape[0], 6)
      self.assertEqual(result["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[1], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[2], "1🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[3], "2🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[4], "2🚫️SPLIT_0")
      self.assertEqual(result["case:concept:name"].iloc[5], "2🚫️SPLIT_0")
      self.assertEqual(log_partition_2.shape[0], 0)
      self.assertEqual(empty_cases_1, 0)
      self.assertEqual(empty_cases_2, 0)

if __name__ == '__main__':
  unittest.main()
