import unittest
from pm4py.objects.process_tree.obj import Operator
import pandas as pd

from optimiist.optimiist_fallthrough.cut_detection.find_cuts_without_filters import sequence_cut_base_model, xor_cut_base_model, parralel_cut_base_model, loop_cut_base_model, findCut_OptIMIIst
from optimiist.util import get_log_statistics

class TestSequenceCutBaseModel(unittest.TestCase):

  def test_sequence_cut_base_model_v1(self):
    efg = {
      ("A", "A"): 0,
      ('A', 'B'): 1,
      ('B', 'A'): 0,
      ('B', 'B'): 0
    }
    activities = ["A", "B"]
    
    partitions, obj_val = sequence_cut_base_model(efg, activities)
    
    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 1)
    self.assertEqual(partitions[0], ['A'])
    self.assertEqual(partitions[1], ['B'])

  def test_sequence_cut_base_model_v2(self):
    """
    Example Trace from EdbA Workshop and Thesis Defence
    """
    efg = {
      ("B", "B"): 0,
      ('B', 'C'): 511,
      ("B", "D"): 500,
      ('C', 'B'): 5,
      ('C', 'C'): 0,
      ('C', 'D'): 0,
      ('D', 'B'): 0,
      ('D', 'C'): 1,
      ('D', 'D'): 0
    }
    activities = ["B", "C", "D"]
    
    partitions, obj_val = sequence_cut_base_model(efg, activities)
    
    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 1006)
    self.assertEqual(partitions[0], ['B'])
    self.assertEqual(partitions[1], ['C', 'D'])

  def test_xor_cut_base_model_v1(self):
    dfg = {
      ("A", "A"): 0,
      ('A', 'B'): 1,
      ('B', 'A'): 0,
      ('B', 'B'): 0
    }
    activities = ["A", "B"]
    partitions, obj_val = xor_cut_base_model(dfg, activities)

    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 1)
    self.assertTrue(partitions[0] == ['A'] and partitions[1] == ['B'] or partitions[1] == ['A'] and partitions[0] == ['B'])

  def test_xor_cut_base_model_v1(self):
    """
    Example DFG from Thesis
    """
    dfg = {
      ("A", "A"): 0,
      ('A', 'B'): 510,
      ("A", "C"): 0,
      ("A", "D"): 0,
      ('B', 'A'): 0,
      ('B', 'B'): 0,
      ('B', 'C'): 10,
      ('B', 'D'): 0,
      ('C', 'A'): 0,
      ('C', 'B'): 0,
      ('C', 'C'): 0,
      ('C', 'D'): 510,
      ('D', 'A'): 10,
      ('D', 'B'): 0,
      ('D', 'C'): 0,
      ('D', 'D'): 0
    }
    activities = ["A", "B", "C", "D"]

    partitions, obj_val = xor_cut_base_model(dfg, activities)
    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 20)
    self.assertTrue(partitions[0] == ['A', 'B'] and partitions[1] == ['C', 'D'] or partitions[1] == ['A', 'B'] and partitions[0] == ['C', 'D'])

  def test_parralel_cut_base_model_v1(self):
    dfg = {
      ("A", "A"): 0,
      ('A', 'B'): 1,
      ('B', 'A'): 1,
      ('B', 'B'): 0
    }
    activities = ["A", "B"]
    start_activities = {"A": 1, "B": 1}
    end_activities = {"A": 1, "B": 1}

    partitions, obj_val = parralel_cut_base_model(dfg, activities, start_activities, end_activities)

    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 2)
    self.assertTrue(partitions[0] == ['A'] and partitions[1] == ['B'] or partitions[1] == ['A'] and partitions[0] == ['B'])

  def test_parralel_cut_base_model_v2(self):
    """
    Example DFG from Thesis
    """
    dfg = {
      ("A", "A"): 0,
      ('A', 'B'): 40,
      ("A", "C"): 0,
      ("A", "D"): 10,
      ('B', 'A'): 0,
      ('B', 'B'): 0,
      ('B', 'C'): 10,
      ('B', 'D'): 30,
      ('C', 'A'): 10,
      ('C', 'B'): 10,
      ('C', 'C'): 0,
      ('C', 'D'): 30,
      ('D', 'A'): 10,
      ('D', 'B'): 20,
      ('D', 'C'): 0,
      ('D', 'D'): 0
    }
    activities = ["A", "B", "C", "D"]
    start_activities = {"A": 30, "B": 0, "C": 40, "D": 0}
    end_activities = {"A": 0, "B": 30, "C": 0, "D": 40}

    partitions, obj_val = parralel_cut_base_model(dfg, activities, start_activities, end_activities)

    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 120)
    
    self.assertTrue(partitions[0] == ['A', 'D'] and partitions[1] == ['B', 'C'] or partitions[1] == ['A', 'D'] and partitions[0] == ['B', 'C'])

  def test_loop_cut_base_model_v1(self):
    dfg = {
      ("A", "A"): 0,
      ('A', 'B'): 5,
      ('B', 'A'): 5,
      ('B', 'B'): 0
    }
    activities = ["A", "B"]
    start_activities = {"A": 1}
    end_activities = {"A": 1}

    partitions, obj_val = loop_cut_base_model(dfg, activities, start_activities, end_activities)

    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 10)
    self.assertTrue(partitions[0] == ['A'] and partitions[1] == ['B'])

  def test_loop_cut_base_model_v2(self):
    """
    Example DFG from Thesis
    """
    dfg = {
      ("A", "A"): 0,
      ('A', 'B'): 21,
      ("A", "C"): 0,
      ("A", "D"): 0,
      ("A", "E"): 0,
      ('B', 'A'): 0,
      ('B', 'B'): 0,
      ('B', 'C'): 22,
      ('B', 'D'): 0,
      ('B', 'E'): 0,
      ('C', 'A'): 0,
      ('C', 'B'): 0,
      ('C', 'C'): 0,
      ('C', 'D'): 11,
      ('C', 'E'): 0,
      ('D', 'A'): 0,
      ('D', 'B'): 1,
      ('D', 'C'): 0,
      ('D', 'D'): 0,
      ('D', 'E'): 10,
      ('E', 'A'): 11,
      ('E', 'B'): 0,
      ('E', 'C'): 0,
      ('E', 'D'): 0,
      ('E', 'E'): 0
    }
    activities = ["A", "B", "C", "D", "E"]
    start_activities = {"A": 10, "E": 1}
    end_activities = {"C": 11}

    partitions, obj_val = loop_cut_base_model(dfg, activities, start_activities, end_activities)

    self.assertEqual(len(partitions), 2)
    self.assertEqual(set(partitions[0] + partitions[1]), set(activities))
    self.assertEqual(obj_val, 30)
    
    self.assertTrue(partitions[0] == ['A', 'B', 'C'] and partitions[1] == ['D', 'E'])  

  def test_findCut_OptIMIIst_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "1", "2"],
      "concept:name": ["A", "B", "A", "B", "D"],
      "time:timestamp": [i for i in range(0, 5)]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    stats = get_log_statistics(log)
    C = findCut_OptIMIIst(stats["dfg"], stats["efg"], stats["start_activities"], stats["end_activities"], stats["activities"])

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