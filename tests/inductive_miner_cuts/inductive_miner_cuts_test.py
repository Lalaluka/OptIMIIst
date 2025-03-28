import unittest
import pandas as pd
from optimiist.inductive_miner_cuts.inductive_miner_cuts import get_inductive_miner_cuts
from pm4py.objects.process_tree.obj import Operator


class TestInductiveMinerCuts(unittest.TestCase):

  def test_get_inductive_miner_cuts_sequence(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 2, 2, 3, 3],
      "concept:name": ["A", "B", "A", "C", "A", "D"],
      "time:timestamp": ["1", "2", "3", "4", "5", "6"]
    })
    operator, partition_1, partition_2 = get_inductive_miner_cuts(log)
    
    self.assertEqual(operator, Operator.SEQUENCE)
    self.assertEqual(len(partition_1), 1)
    self.assertEqual(len(partition_2), 3)
    self.assertEqual(partition_1[0], "A")
    self.assertEqual(sorted(partition_2), sorted(["B", "C", "D"]))

  def test_get_inductive_miner_cuts_parallel(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 2, 2, 3, 3],
      "concept:name": ["A", "B", "B", "A", "A", "B"],
      "time:timestamp": ["1", "2", "3", "4", "5", "6"]
    })
    operator, partition_1, partition_2 = get_inductive_miner_cuts(log)
    
    self.assertEqual(operator, Operator.PARALLEL)
    self.assertEqual(len(partition_1), 1)
    self.assertEqual(len(partition_2), 1)
    self.assertEqual(partition_1[0], "A")
    self.assertEqual(partition_2, ["B"])

  def test_get_inductive_miner_cuts_loop(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 1, 2, 2, 2],
      "concept:name": ["A", "B", "A", "A", "B", "A"],
      "time:timestamp": ["1", "2", "3", "4", "5", "6"]
    })
    operator, partition_1, partition_2 = get_inductive_miner_cuts(log)
    
    self.assertEqual(operator, Operator.LOOP)
    self.assertEqual(len(partition_1), 1)
    self.assertEqual(len(partition_2), 1)
    self.assertEqual(partition_1[0], "A")
    self.assertEqual(partition_2, ["B"])

  def test_get_inductive_miner_cuts_xor(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 2, 2, 3, 3],
      "concept:name": ["A", "B", "C", "D", "A", "B"],
      "time:timestamp": ["1", "2", "3", "4", "5", "6"]
    })
    operator, partition_1, partition_2 = get_inductive_miner_cuts(log)
    
    self.assertEqual(operator, Operator.XOR)
    self.assertEqual(len(partition_1), 2)
    self.assertEqual(len(partition_2), 2)
    self.assertTrue(
        (sorted(partition_1) == sorted(["A", "B"]) and sorted(partition_2) == sorted(["C", "D"])) or
        (sorted(partition_1) == sorted(["C", "D"]) and sorted(partition_2) == sorted(["A", "B"]))
    )

  def test_get_inductive_miner_cuts_empty_log(self):
    empty_log = pd.DataFrame(columns=["case:concept:name", "concept:name", "time:timestamp"])
    res = get_inductive_miner_cuts(empty_log)
    
    self.assertIsNone(res)

if __name__ == '__main__':
  unittest.main()