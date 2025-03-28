import unittest
import pandas as pd
from pm4py.objects.process_tree.obj import Operator
from optimiist.split_log.split_log import split_log

class TestSplitLog(unittest.TestCase):

  def setUp(self):
    # Sample log data for testing
    self.log = pd.DataFrame({
      'case:concept:name': [1, 1, 1, 2, 2, 2],
      'concept:name': ['A', 'B', 'A', 'C', 'B', 'C']
    })

  def test_tau_skip(self):
    log, empty_df, empty_traces_1, empty_traces_2 = split_log(self.log, Operator.XOR, ['A', 'B', 'C'], [], 100)
    self.assertTrue(log.equals(self.log))
    self.assertTrue(empty_df.empty)
    self.assertEqual(empty_traces_1, 0)
    self.assertEqual(empty_traces_2, 0)

  def test_tau_loop(self):
    log1, log2, empty_traces_1, empty_traces_2 = split_log(self.log, Operator.LOOP, ['A', 'B', 'C'], [], 100)

    self.assertEqual(log1.shape[0], 6)
    self.assertEqual(log2.shape[0], 0)
    self.assertEqual(empty_traces_1, 100)
    self.assertEqual(empty_traces_2, 0)

  def test_loop(self):
    log_1, log_2, empty_traces_1, empty_traces_2 = split_log(self.log, Operator.LOOP, ['A', 'C'], ['B'], 100)
    self.assertEqual(empty_traces_1, 100)
    self.assertEqual(empty_traces_2, 0)

    self.assertEqual(log_1.shape[0], 4)
    self.assertEqual(log_2.shape[0], 2)

    self.assertEqual(log_1["concept:name"].iloc[0], "A")
    self.assertEqual(log_1["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(log_1["concept:name"].iloc[1], "A")
    self.assertEqual(log_1["case:concept:name"].iloc[1], "1🚫️SPLIT_1")
    self.assertEqual(log_1["concept:name"].iloc[2], "C")
    self.assertEqual(log_1["case:concept:name"].iloc[2], "2🚫️SPLIT_0")
    self.assertEqual(log_1["concept:name"].iloc[3], "C")
    self.assertEqual(log_1["case:concept:name"].iloc[3], "2🚫️SPLIT_1")
    self.assertEqual(log_2["concept:name"].iloc[0], "B")
    self.assertEqual(log_2["case:concept:name"].iloc[0], "1🚫️SPLIT_0")
    self.assertEqual(log_2["concept:name"].iloc[1], "B")
    self.assertEqual(log_2["case:concept:name"].iloc[1], "2🚫️SPLIT_0")

  def test_xor_v1(self):
    log1, log2, empty_traces_1, empty_traces_2 = split_log(self.log, Operator.XOR, ['A', 'C'], ['B'], 100)
    
    self.assertEqual(empty_traces_1, 100)
    self.assertEqual(empty_traces_2, 0)
    self.assertEqual(log1.shape[0], 4)
    self.assertEqual(log2.shape[0], 2)

    self.assertEqual(log1["concept:name"].iloc[0], "A")
    self.assertEqual(log1["case:concept:name"].iloc[0], 1)
    self.assertEqual(log1["concept:name"].iloc[1], "A")
    self.assertEqual(log1["case:concept:name"].iloc[1], 1)
    self.assertEqual(log1["concept:name"].iloc[2], "C")
    self.assertEqual(log1["case:concept:name"].iloc[2], 2)
    self.assertEqual(log1["concept:name"].iloc[3], "C")
    self.assertEqual(log1["case:concept:name"].iloc[3], 2)
    self.assertEqual(log2["concept:name"].iloc[0], "B")
    self.assertEqual(log2["case:concept:name"].iloc[0], 1)
    self.assertEqual(log2["concept:name"].iloc[1], "B")
    self.assertEqual(log2["case:concept:name"].iloc[1], 2)

  def test_xor_v2(self):
    log = pd.DataFrame({
      'case:concept:name': [1, 1, 1, 2, 2, 2],
      'concept:name': ['A', 'A', 'A', 'C', 'B', 'C']
    })

    log1, log2, empty_traces_1, empty_traces_2 = split_log(log, Operator.XOR, ['A', 'C'], ['B'], 0)

    self.assertEqual(empty_traces_1, 0)
    self.assertEqual(empty_traces_2, 0)
    self.assertEqual(log1.shape[0], 5)
    self.assertEqual(log2.shape[0], 1)

  def test_sequence_green(self):
    log = pd.DataFrame({
      'case:concept:name': [1, 1, 1, 2, 2, 2],
      'concept:name': ['A', 'B', 'C', 'A', 'B', 'C']
    })

    log1, log2, empty_traces_1, empty_traces_2 = split_log(log, Operator.SEQUENCE, ['A', 'B'], ['C'], 0)

    self.assertEqual(empty_traces_1, 0)
    self.assertEqual(empty_traces_2, 0)
    self.assertEqual(log1.shape[0], 4)
    self.assertEqual(log2.shape[0], 2)

    self.assertEqual(log1["concept:name"].iloc[0], "A")
    self.assertEqual(log1["case:concept:name"].iloc[0], 1)
    self.assertEqual(log1["concept:name"].iloc[1], "B")
    self.assertEqual(log1["case:concept:name"].iloc[1], 1)
    self.assertEqual(log1["concept:name"].iloc[2], "A")
    self.assertEqual(log1["case:concept:name"].iloc[2], 2)
    self.assertEqual(log1["concept:name"].iloc[3], "B")
    self.assertEqual(log1["case:concept:name"].iloc[3], 2)
    self.assertEqual(log2["concept:name"].iloc[0], "C")
    self.assertEqual(log2["case:concept:name"].iloc[0], 1)
    self.assertEqual(log2["concept:name"].iloc[1], "C")
    self.assertEqual(log2["case:concept:name"].iloc[1], 2)
  
  def test_sequence_red(self):
    log = pd.DataFrame({
      'case:concept:name': [1, 1, 1, 2, 2, 2],
      'concept:name': ['A', 'B', 'C', 'A', 'B', 'D']
    })

    log1, log2, empty_traces_1, empty_traces_2 = split_log(log, Operator.SEQUENCE, ['A', 'B', 'C'], ['D'], 0)

    self.assertEqual(empty_traces_1, 0)
    self.assertEqual(empty_traces_2, 1)
    self.assertEqual(log1.shape[0], 5)
    self.assertEqual(log2.shape[0], 1)

    self.assertEqual(log1["concept:name"].iloc[0], "A")
    self.assertEqual(log1["case:concept:name"].iloc[0], 1)
    self.assertEqual(log1["concept:name"].iloc[1], "B")
    self.assertEqual(log1["case:concept:name"].iloc[1], 1)
    self.assertEqual(log1["concept:name"].iloc[2], "C")
    self.assertEqual(log1["case:concept:name"].iloc[2], 1)
    self.assertEqual(log1["concept:name"].iloc[3], "A")
    self.assertEqual(log1["case:concept:name"].iloc[3], 2)
    self.assertEqual(log1["concept:name"].iloc[4], "B")
    self.assertEqual(log1["case:concept:name"].iloc[4], 2)
    self.assertEqual(log2["concept:name"].iloc[0], "D")
    self.assertEqual(log2["case:concept:name"].iloc[0], 2)

  def test_parallel_green(self):
    log = pd.DataFrame({
      'case:concept:name': [1, 1, 1, 2, 2, 2],
      'concept:name': ['A', 'B', 'C', 'A', 'B', 'C']
    })

    log1, log2, empty_traces_1, empty_traces_2 = split_log(log, Operator.PARALLEL, ['A', 'B'], ['C'], 0)

    self.assertEqual(empty_traces_1, 0)
    self.assertEqual(empty_traces_2, 0)
    self.assertEqual(log1.shape[0], 4)
    self.assertEqual(log2.shape[0], 2)

    self.assertEqual(log1["concept:name"].iloc[0], "A")
    self.assertEqual(log1["case:concept:name"].iloc[0], 1)
    self.assertEqual(log1["concept:name"].iloc[1], "B")
    self.assertEqual(log1["case:concept:name"].iloc[1], 1)
    self.assertEqual(log1["concept:name"].iloc[2], "A")
    self.assertEqual(log1["case:concept:name"].iloc[2], 2)
    self.assertEqual(log1["concept:name"].iloc[3], "B")
    self.assertEqual(log1["case:concept:name"].iloc[3], 2)
    self.assertEqual(log2["concept:name"].iloc[0], "C")
    self.assertEqual(log2["case:concept:name"].iloc[0], 1)
    self.assertEqual(log2["concept:name"].iloc[1], "C")
    self.assertEqual(log2["case:concept:name"].iloc[1], 2)

  def test_parallel_red(self):
    log = pd.DataFrame({
      'case:concept:name': [1, 1, 1, 2, 2, 2],
      'concept:name': ['A', 'B', 'C', 'A', 'D', 'B']
    })

    log1, log2, empty_traces_1, empty_traces_2 = split_log(log, Operator.PARALLEL, ['A', 'B', "D"], ['C'], 0)

    self.assertEqual(empty_traces_1, 0)
    self.assertEqual(empty_traces_2, 1)
    self.assertEqual(log1.shape[0], 5)
    self.assertEqual(log2.shape[0], 1)

    self.assertEqual(log1["concept:name"].iloc[0], "A")
    self.assertEqual(log1["case:concept:name"].iloc[0], 1)
    self.assertEqual(log1["concept:name"].iloc[1], "B")
    self.assertEqual(log1["case:concept:name"].iloc[1], 1)
    self.assertEqual(log1["concept:name"].iloc[2], "A")
    self.assertEqual(log1["case:concept:name"].iloc[2], 2)
    self.assertEqual(log1["concept:name"].iloc[3], "D")
    self.assertEqual(log1["case:concept:name"].iloc[3], 2)
    self.assertEqual(log1["concept:name"].iloc[4], "B")
    self.assertEqual(log1["case:concept:name"].iloc[4], 2)
    self.assertEqual(log2["concept:name"].iloc[0], "C")
    self.assertEqual(log2["case:concept:name"].iloc[0], 1)


if __name__ == '__main__':
  unittest.main()