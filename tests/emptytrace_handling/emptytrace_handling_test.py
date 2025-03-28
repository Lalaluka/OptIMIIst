import unittest
import pandas as pd
from pm4py.objects.process_tree.obj import Operator

from optimiist.emptytrace_handling.emptytrace_handling import handle_empty_traces

class TestEmptyTraceHandling(unittest.TestCase):
  def test_handle_empty_traces_empty_log(self):
    result = handle_empty_traces(pd.DataFrame(columns=["case:concept:name"]), 0)
    self.assertEqual(result, None)

  def test_handle_empty_traces_no_skip_no_loop(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1", "case2", "case3", "case4", "case5"],
      "concept:name": ["A", "B", "C", "D", "E"],
      "time:timestamp": ["2023-01-01T09:00:00.000+00:00",
                         "2023-01-01T10:00:00.000+00:00",
                         "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T12:00:00.000+00:00",
                         "2023-01-01T13:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = handle_empty_traces(log, 0)
    self.assertEqual(result, None)

  @unittest.skip
  def test_handle_empty_traces_no_skip_no_loop(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1", "case1", "case3", "case4", "case5"],
      "concept:name": ["A", "A", "C", "D", "E"],
      "time:timestamp": ["2023-01-01T09:00:00.000+00:00",
                         "2023-01-01T10:00:00.000+00:00",
                         "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T12:00:00.000+00:00",
                         "2023-01-01T13:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = handle_empty_traces(log, 0)
    self.assertEqual(result[0], Operator.LOOP)
    self.assertEqual(sorted(result[1]), sorted(["A", "C", "D", "E"]))
    self.assertEqual(result[2], [])

  def test_handle_empty_traces_skip_no_loop(self):
    log = pd.DataFrame({
      "case:concept:name": ["case1", "case1", "case3", "case4", "case5", "case6", "case7", "case8", "case9", "case10"],
      "concept:name": ["A", "A", "C", "D", "E", "A", "A", "C", "D", "E"],
      "time:timestamp": ["2023-01-01T09:00:00.000+00:00",
                         "2023-01-01T10:00:00.000+00:00",
                         "2023-01-01T11:00:00.000+00:00",
                         "2023-01-01T12:00:00.000+00:00",
                         "2023-01-01T13:00:00.000+00:00",
                         "2023-01-01T14:00:00.000+00:00",
                         "2023-01-01T15:00:00.000+00:00",
                         "2023-01-01T16:00:00.000+00:00",
                         "2023-01-01T17:00:00.000+00:00",
                         "2023-01-01T18:00:00.000+00:00"]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = handle_empty_traces(log, 500)
    self.assertEqual(result[0], Operator.XOR)
    self.assertEqual(sorted(result[1]), sorted(["A", "C", "D", "E"]))
    self.assertEqual(result[2], [])

  @unittest.skip
  def test_handle_empty_traces_skip_and_loop(self):
    log = pd.DataFrame({
        "case:concept:name": ["case1", "case1", "case2", "case2", "case3", "case3", "case4", "case5", "case6", "case7"],
        "concept:name": ["A", "A", "A", "A", "A", "A", "A", "C", "D", "E"],
        "time:timestamp": ["2023-01-01T09:00:00.000+00:00",
                             "2023-01-01T10:00:00.000+00:00",
                             "2023-01-01T11:00:00.000+00:00",
                             "2023-01-01T12:00:00.000+00:00",
                             "2023-01-01T13:00:00.000+00:00",
                             "2023-01-01T14:00:00.000+00:00",
                             "2023-01-01T15:00:00.000+00:00",
                             "2023-01-01T16:00:00.000+00:00",
                             "2023-01-01T17:00:00.000+00:00",
                             "2023-01-01T18:00:00.000+00:00"]
        })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    result = handle_empty_traces(log, 20)

    self.assertEqual(result[0], Operator.LOOP)
    self.assertEqual(sorted(result[1]), [])
    self.assertEqual(result[2], sorted(["A", "C", "D", "E"]))

if __name__ == '__main__':
  unittest.main()
