import unittest
from pm4py.objects.process_tree.obj import ProcessTree, Operator
from optimiist.optimiist_fallthrough.optimiist_fallthrough import get_optimiist_cut
import pandas as pd

class TestOptimiistFallthrough(unittest.TestCase):

  def test_get_optimiist_cut_without_filter(self):
    log_seq = pd.DataFrame({
      "case:concept:name": ["case1", "case1", "case1", "case2", "case2", "case2"],
      "concept:name": ["A", "B", "C", "A", "B", "C"],
      "time:timestamp": ["2023-01-01T10:00:00.000+00:00", 
                         "2023-01-01T11:00:00.000+00:00", 
                         "2023-01-01T12:00:00.000+00:00", 
                         "2023-01-01T10:00:00.000+00:00", 
                         "2023-01-01T11:00:00.000+00:00", 
                         "2023-01-01T12:00:00.000+00:00"]
    })
    log_seq["time:timestamp"] = pd.to_datetime(log_seq["time:timestamp"])
    result = get_optimiist_cut(log_seq, filter=False)

    self.assertIsInstance(result[0], Operator)
    self.assertIsInstance(result[1], pd.DataFrame)
    self.assertIsInstance(result[2], pd.DataFrame)

    self.assertEqual(result[0], Operator.SEQUENCE)
    

  def test_get_optimiist_cut_xor(self):
    log_xor = pd.DataFrame({
      "case:concept:name": ["case1", "case1", "case1", "case2", "case2", "case2"],
      "concept:name": ["A", "B", "C", "D", "E", "F"],
      "time:timestamp": ["2023-01-01T10:00:00.000+00:00", 
                         "2023-01-01T11:00:00.000+00:00", 
                         "2023-01-01T12:00:00.000+00:00", 
                         "2023-01-01T10:00:00.000+00:00", 
                         "2023-01-01T11:00:00.000+00:00", 
                         "2023-01-01T12:00:00.000+00:00"]
    })
    log_xor["time:timestamp"] = pd.to_datetime(log_xor["time:timestamp"])

    result = get_optimiist_cut(log_xor, empty_traces=5, filter=False)

    self.assertIsInstance(result[0], Operator)
    self.assertIsInstance(result[1], pd.DataFrame)
    self.assertIsInstance(result[2], pd.DataFrame)

    self.assertEqual(result[0], Operator.XOR)
    
if __name__ == '__main__':
  unittest.main()