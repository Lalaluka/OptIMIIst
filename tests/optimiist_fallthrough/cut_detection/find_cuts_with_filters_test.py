import unittest
from optimiist.optimiist_fallthrough.cut_detection.find_cuts_with_filters import get_filtered_parallel_cut, get_filtered_xor_cut, sequence_cut_filter_model, get_filtered_sequence_cut, build_skip_dfg, xor_cut_filter_model, parralel_cut_filter_model, loop_cut_filter_model, findCut_OptIMIIst
import pandas as pd
from pm4py.objects.process_tree.obj import Operator
from optimiist.util import get_log_statistics

class TestFindCutsWithFilters(unittest.TestCase):
  def test_sequence_cut_filter_model_v1(self):
    activities = ["A", "B", "C"]
    efg = {
      ("A", "A"): 0,
      ("A", "B"): 1,
      ("A", "C"): 1,
      ("B", "A"): 0,
      ("B", "B"): 0,
      ("B", "C"): 0,
      ("C", "A"): 1,
      ("C", "B"): 0,
      ("C", "C"): 0
    }
    partitions, filtered_activity, objective_value = sequence_cut_filter_model(efg, activities, verb=0)

    # Check if partitions are correctly identified
    self.assertIsInstance(partitions, tuple)
    self.assertEqual(len(partitions), 2)
    self.assertTrue(all(activity in activities for activity in partitions[0] + partitions[1]))

    self.assertEqual(filtered_activity, "C")

  def test_sequence_cut_filter_model_v2(self):
    activities = ["A", "B", "C"]
    efg = {
      ("A", "A"): 0,
      ("A", "B"): 1,
      ("A", "C"): 0,
      ("B", "A"): 0,
      ("B", "B"): 0,
      ("B", "C"): 0,
      ("C", "A"): 0,
      ("C", "B"): 0,
      ("C", "C"): 0
    }
    partitions, filtered_activity, objective_value = sequence_cut_filter_model(efg, activities, verb=0)
    
    # Check if partitions are correctly identified
    self.assertIsInstance(partitions, tuple)
    self.assertEqual(len(partitions), 2)
    self.assertTrue(all(activity in activities for activity in partitions[0] + partitions[1]))

    self.assertEqual(filtered_activity, "C")

  def test_get_filtered_sequence_cut_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9", "9"],
      "concept:name": ["A", "B", "A", "C", "C", "A", "A", "B", "A", "B", "A", "B", "A", "B", "A", "B", "C", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    })
    activities = ["A", "B", "C"]
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    partitions = get_filtered_sequence_cut(log, get_log_statistics(log))

    self.assertEqual(partitions[1], ["C"])
    self.assertTrue(partitions[0][0], ["A"])
    self.assertTrue(partitions[0][1], ["B"])

  def test_get_filtered_sequence_cut_v2(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "2", "2", "3", "3"],
      "concept:name": ["A", "B", "A", "C", "A", "C"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    activities = ["A", "B", "C"]
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    partitions = get_filtered_sequence_cut(log, get_log_statistics(log))

    self.assertEqual(partitions[1], [])
    self.assertTrue(partitions[0][0], ["A"])
    self.assertTrue(partitions[0][1], ["B"])

  def test_build_skip_dfg(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", 
                            "2", "2", 
                            "3", "3", "3", 
                            "4", "4", "4", "4",
                            "5"],
      "concept:name": ["A", "B",
                        "A", "C", 
                        "A", "C", "B", 
                        "A", "A", "C", "C",
                        "C"],
      "time:timestamp": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    })
    activities = ["A", "B", "C"]
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])

    one_skip_dfg, skips, start_activities, end_activities = build_skip_dfg(log, activities)

    self.assertEqual(one_skip_dfg[("A", "C")], 3)
    self.assertEqual(skips[("C", ("A", "B"))], 1)
    self.assertEqual(start_activities, {'A': {'B': 1, 'C': 4}, 'B': {"A": 4, "C": 1}, 'C': {"A": 4}})
    self.assertEqual(end_activities, {'A': {'B': 2, 'C': 3}, 'B': {'C': 4, 'A': 1}, 'C': {'B': 2, 'A': 2}})    

  def test_xor_cut_filter_model_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "2", "2", "3", "3", "3"],
      "concept:name": ["A", "B", "D", "C", "A", "B", "C"],
      "time:timestamp": [1, 2, 3, 4, 5, 6, 7]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C", "D"]
    partitions, filtered_activity, objective_value = xor_cut_filter_model(log, activities, verb=0)

    self.assertIsInstance(partitions, tuple)
    self.assertEqual(len(partitions), 2)
    self.assertTrue(all(activity in activities for activity in partitions[0] + partitions[1]))

    self.assertEqual(filtered_activity, "C")
    self.assertEqual(objective_value, 0)

  def test_xor_cut_filter_model_v2(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", 
                            "2", "2", 
                            "3", "3", 
                            "4", "4", "4",
                            "5", "5",
                            "6", "6",
                            "7", "7",
                            "8", "8", "8"],
      "concept:name": ["A", "C", 
                       "A", "C", 
                       "A", "C", 
                       "A", "B", "C",
                       "D", "E",
                       "D", "E",
                       "D", "E",
                       "D", "B", "E"],
      "time:timestamp": [i for i in range(0, 18)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C", "D", "E"]
    partitions, filtered_activity, objective_value = xor_cut_filter_model(log, activities, verb=0)

    self.assertIsInstance(partitions, tuple)
    self.assertEqual(len(partitions), 2)
    self.assertTrue(all(activity in activities for activity in partitions[0] + partitions[1]))

    self.assertEqual(filtered_activity, "B")
    self.assertEqual(objective_value, 0)

  def test_xor_cut_filter_model_v3(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", 
                            "2", "2", 
                            "3", "3", 
                            "4", "4", "4",
                            "10", "10", "10",
                            "5", "5",
                            "6", "6",
                            "7", "7",
                            "8", "8", "8"],
      "concept:name": ["A", "C", 
                       "A", "C", 
                       "A", "C", 
                       "A", "B", "C",
                       "A", "B", "C",
                       "D", "E",
                       "D", "E",
                       "D", "E",
                       "D", "B", "E"],
      "time:timestamp": [i for i in range(0, 21)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C", "D", "E"]
    partitions, filtered_activity, objective_value = xor_cut_filter_model(log, activities, verb=0)

    self.assertIsInstance(partitions, tuple)
    self.assertEqual(len(partitions), 2)
    self.assertTrue(all(activity in activities for activity in partitions[0] + partitions[1]))

    self.assertEqual(filtered_activity, "B")
    self.assertEqual(objective_value, 0)

  def test_get_filtered_xor_cut(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", 
                            "2", "2", 
                            "3", "3", 
                            "4", "4", "4",
                            "10", "10", "10",
                            "5", "5",
                            "6", "6",
                            "7", "7",
                            "8", "8", "8",
                            "9", "9"],
      "concept:name": ["A", "C", 
                       "A", "C", 
                       "A", "C", 
                       "A", "B", "C",
                       "A", "B", "C",
                       "D", "E",
                       "D", "E",
                       "D", "E",
                       "D", "B", "E",
                       "C", "D"],
      "time:timestamp": [i for i in range(0, 23)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C", "D", "E"]

    log_statistics = get_log_statistics(log)

    partitions = get_filtered_xor_cut(log, log_statistics)

  def test_parralel_cut_filter_model_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", 
                            "2", "2"],
      "concept:name": ["A", "B", "A",
                       "C", "C",],
      "time:timestamp": [i for i in range(0, 5)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C"]
    partitions, filtered, objective_value = parralel_cut_filter_model(log, activities)

    self.assertEqual(filtered, "C")
    self.assertEqual(objective_value, 2)
    # A and C are in different partitions
    self.assertTrue("A" in partitions[0] and "B" in partitions[1] or "A" in partitions[1] and "b" in partitions[0])

  def test_parralel_cut_filter_model_v2(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1",
                            "2", "2", "2",
                            "3"],
      "concept:name": ["A", "B", "C",
                       "A", "C", "B",
                       "D"],
      "time:timestamp": [i for i in range(0, 7)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C", "D"]
    partitions, filtered, objective_value = parralel_cut_filter_model(log, activities)

    self.assertEqual(filtered, "D")
    self.assertEqual(objective_value, 3)

  def test_parralel_cut_filter_model_v3(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1","1",
                            "2", "2", "2","2",
                            "3", "3", "3","3",
                            "4", "4", "4","4"],
      "concept:name": ["A", "B", "C","A",
                       "A", "C", "B","A",
                       "A", "B", "C","A",
                       "A", "C", "A", "A"],
      "time:timestamp": [i for i in range(0, 16)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C"]
    partitions, filtered, objective_value = parralel_cut_filter_model(log, activities)

    self.assertEqual(filtered, "B")
    self.assertEqual(objective_value, 8)

  def test_get_filtered_parallel_cut_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1","1",
                            "2", "2", "2","2",
                            "3", "3", "3","3",
                            "4", "4", "4","4"],
      "concept:name": ["A", "B", "C","A",
                       "A", "C", "B","A",
                       "A", "B", "C","A",
                       "A", "C", "A", "A"],
      "time:timestamp": [i for i in range(0, 16)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "C"]
    partitions, filtered = get_filtered_parallel_cut(log, get_log_statistics(log))

    self.assertEqual(filtered, [])

  def test_loop_cut_filter_model_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "2"],
      "concept:name": ["A", "B", "A", "D"],
      "time:timestamp": [i for i in range(0, 4)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    activities = ["A", "B", "D"]
    partitions, filtered, objective_value = loop_cut_filter_model(log, activities)

    self.assertEqual(filtered, "D")
    self.assertEqual(objective_value, 2)

  def test_findCut_OptIMIIst_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "1", "2"],
      "concept:name": ["A", "B", "A", "B", "D"],
      "time:timestamp": [i for i in range(0, 5)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    C = findCut_OptIMIIst(log, get_log_statistics(log))

    self.assertEqual(C[0][0], Operator.SEQUENCE)
    self.assertEqual(C[0][1], ["A"])
    self.assertEqual(C[1][0], Operator.XOR)
    self.assertIsNot(C[1][1], Operator)
    self.assertEqual(C[2][0], Operator.PARALLEL)
    self.assertIsNot(C[2][1], Operator)
    self.assertEqual(C[3][0], Operator.LOOP)
    self.assertIsNot(C[3][1], Operator)

if __name__ == '__main__':
  unittest.main()