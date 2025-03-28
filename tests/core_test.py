import unittest
import pandas as pd
from pm4py.objects.process_tree.obj import ProcessTree, Operator

from optimiist.core import optimiist_rec

class TestCore(unittest.TestCase):
  def test_recursion_base_case_log(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1"],
      "concept:name": ["A"],
      "time:timestamp": ["2023-01-01T10:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = optimiist_rec(log)
    self.assertEqual(result,ProcessTree(label="A", children=[]))

  def test_recursion_base_case_empty_log(self):
    log = pd.DataFrame(columns=["case:concept:name", "concept:name"])
    result = optimiist_rec(log)
    self.assertEqual(result,ProcessTree(children=[]))

  def test_recursion_seq_cut(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1", "case1"],
      "concept:name": ["A", "B"],
      "time:timestamp": ["2023-01-01T10:00:00.000+00:00", "2023-01-01T11:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = optimiist_rec(log)
    self.assertEqual(str(result), "->( 'A', 'B' )")

  def test_recursion_seq_cut_xor_cut(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1", "case1", "case2", "case2"],
      "concept:name": ["A", "B", "A", "C"],
      "time:timestamp": ["2023-01-01T10:00:00.000+00:00", 
                         "2023-01-01T11:00:00.000+00:00", 
                         "2023-01-01T10:00:00.000+00:00", 
                         "2023-01-01T11:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = optimiist_rec(log)

    self.assertEqual(result.operator, Operator.SEQUENCE)
    self.assertEqual(result.children[1].operator, Operator.XOR)

    self.assertTrue(
        (result.children[1].children[0].label == "B" and result.children[1].children[1].label == "C") or
        (result.children[1].children[0].label == "C" and result.children[1].children[1].label == "B")
    )
    self.assertEqual(result.children[0].label, "A")

  def test_recursion_fallthrough(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1", "case1", "case1", 
                            "case2", "case2", 
                            "case3", "case3", 
                            "case4", "case4",
                            "case5", "case5",
                            "case6", "case6",
                            "case7", "case7",
                            "case8", "case8", "case8", "case8"],
      "concept:name": ["A", "B", "C", 
                       "A", "B", 
                       "A", "B", 
                       "A", "B", 
                       "A", "C",
                       "A", "C",
                       "A", "C",
                       "A", "C", "A", "C"],
      "time:timestamp": ["2023-01-01T10:00:00.000+00:00", "2023-01-01T11:00:00.000+00:00", "2023-01-01T12:00:00.000+00:00", 
                         "2023-01-01T10:00:00.000+00:00", "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T10:00:00.000+00:00", "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T12:00:00.000+00:00", "2023-01-01T13:00:00.000+00:00",
                         "2023-01-01T14:00:00.000+00:00", "2023-01-01T15:00:00.000+00:00",
                         "2023-01-01T10:00:00.000+00:00", "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T10:00:00.000+00:00", "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T12:00:00.000+00:00", "2023-01-01T13:00:00.000+00:00", "2023-01-01T14:00:00.000+00:00", "2023-01-01T15:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = optimiist_rec(log)
    
    self.assertEqual(result.operator, Operator.SEQUENCE)

if __name__ == '__main__':
  unittest.main()
