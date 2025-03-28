import unittest
import numpy as np
import pandas as pd
from optimiist.optimiist_fallthrough.cut_quality import calculate_mae, f1_score, get_seq_conformance, get_xor_conformance, get_and_conformance, get_loop_conformance, get_tau_loop_confromance

class TestCutQuality(unittest.TestCase):
  def test_calculate_mae_same_length(self):
    truth_array = [1, 2, 3, 4, 5]
    input_array = [1, 2, 3, 4, 5]
    result = calculate_mae(truth_array, input_array)
    self.assertEqual(result, 0.0)
    
    input_array = [2, 3, 4, 5, 6]
    result = calculate_mae(truth_array, input_array)
    self.assertEqual(result, 1.0)

  def test_calculate_mae_f1_score(self):
    fitness = 0.8
    precision = 0.9
    result = f1_score(precision, fitness)
    self.assertEqual(result, 0.8470588235294118)
    fitness = 0.5
    precision = 0.5
    result = f1_score(precision, fitness)
    self.assertEqual(result, 0.5)

  def test_get_seq_conformance_v1(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 1,
      ("b", "a"): 0,
      ("b", "b"): 0
    }
    partition_1 = ["a"]
    partition_2 = ["b"]

    log_1 = pd.DataFrame({
      "case:concept:name": ["1"],
      "concept:name": ["a"],
      "time:timestamp": [1]
    })
    log_1["time:timestamp"] = pd.to_datetime(log_1["time:timestamp"])

    log_2 = pd.DataFrame({
      "case:concept:name": ["1"],
      "concept:name": ["b"],
      "time:timestamp": [2]
    })
    log_2["time:timestamp"] = pd.to_datetime(log_2["time:timestamp"])

    result = get_seq_conformance(dfg, partition_1, partition_2, log_1, log_2)
    self.assertEqual(result, (1.0, 1.0, 1.1))

  def test_get_seq_conformance_v2(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 1,
      ("b", "a"): 1,
      ("b", "b"): 0
    }
    partition_1 = ["a"]
    partition_2 = ["b"]

    log_1 = pd.DataFrame({
      "case:concept:name": ["1"],
      "concept:name": ["a"],
      "time:timestamp": [1]
    })
    log_1["time:timestamp"] = pd.to_datetime(log_1["time:timestamp"])

    log_2 = pd.DataFrame({
      "case:concept:name": ["1"],
      "concept:name": ["b"],
      "time:timestamp": [2]
    })
    log_2["time:timestamp"] = pd.to_datetime(log_2["time:timestamp"])

    result = get_seq_conformance(dfg, partition_1, partition_2, log_1, log_2)
    self.assertEqual(result[0], 0.5)
    self.assertEqual(result[1], 1)
    self.assertAlmostEqual(result[2], 0.7333333333333334, places=2)

  def test_get_seq_conformance_v3(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 1,
      ("a", "c"): 2,
      ("b", "a"): 0,
      ("b", "b"): 0,
      ("b", "c"): 0,
      ("c", "a"): 0,
      ("c", "b"): 0,
      ("c", "c"): 0
    }
    partition_1 = ["a"]
    partition_2 = ["b", "c"]

    log_1 = pd.DataFrame({
      "case:concept:name": ["1", "2", "3"],
      "concept:name": ["a", "a", "a"],
      "time:timestamp": [1, 2, 3]
    })
    log_1["time:timestamp"] = pd.to_datetime(log_1["time:timestamp"])

    log_2 = pd.DataFrame({
      "case:concept:name": ["1", "2", "3"],
      "concept:name": ["b", "c", "c"],
      "time:timestamp": [4, 5, 6]
    })
    log_2["time:timestamp"] = pd.to_datetime(log_2["time:timestamp"])

    result = get_seq_conformance(dfg, partition_1, partition_2, log_1, log_2)
    self.assertEqual(result[0], 1)
    self.assertEqual(result[1], 1)
    self.assertAlmostEqual(result[2], 1, places=2)

  def test_get_seq_conformance_v3(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 0,
      ("a", "c"): 100,
      ("a", "d"): 0,
      ("b", "a"): 0,
      ("b", "b"): 0,
      ("b", "c"): 5,
      ("b", "d"): 100,
      ("c", "a"): 0,
      ("c", "b"): 0,
      ("c", "c"): 0,
      ("c", "d"): 50,
      ("d", "a"): 5,
      ("d", "b"): 0,
      ("d", "c"): 0,
      ("d", "d"): 0
    }
    partition_1 = ["a", "b"]
    partition_2 = ["c", "d"]

    log_1 = pd.DataFrame({
        "case:concept:name": [],
        "concept:name": [],
        "time:timestamp": []
    })

    log_1 = pd.concat([log_1, pd.DataFrame({
      "case:concept:name": [str(i) for i in range(0, 100)],
      "concept:name": ["a"] * 100,
      "time:timestamp": range(0, 100)
    })], ignore_index=True)

    log_1 = pd.concat([log_1, pd.DataFrame({
        "case:concept:name": [str(i) for i in range(100, 205)],
        "concept:name": ["b"] * 105,
        "time:timestamp": range(100, 205)
    })], ignore_index=True)

    log_1["time:timestamp"] = pd.to_datetime(log_1["time:timestamp"])

    log_2 = pd.DataFrame({
        "case:concept:name": [],
        "concept:name": [],
        "time:timestamp": []
    })

    log_2 = pd.concat([log_2, pd.DataFrame({
        "case:concept:name": [str(i) for i in range(0, 100)],
        "concept:name": ["d"] * 100,
        "time:timestamp": range(0, 100)
    })], ignore_index=True)

    log_2 = pd.concat([log_2, pd.DataFrame({
        "case:concept:name": [str(i) for i in range(100, 205)],
        "concept:name": ["c"] * 105,
        "time:timestamp": range(100, 205)
    })], ignore_index=True)

    log_2["time:timestamp"] = pd.to_datetime(log_2["time:timestamp"])

    result = get_seq_conformance(dfg, partition_1, partition_2, log_1, log_2)
    self.assertEqual(result[0], 0.9761904761904762)
    self.assertEqual(result[1], 0.5238095238095238)
    self.assertAlmostEqual(result[2], 0.7499622071050642, places=2)

  def test_get_xor_conformance_v1(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 0,
      ("b", "a"): 0,
      ("b", "b"): 0
    }
    partition_1 = ["a"]
    partition_2 = ["b"]

    result = get_xor_conformance(dfg, partition_1, partition_2)
    self.assertEqual(result, (1, 1, 1))

  def test_get_xor_conformance_v2(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 1,
      ("b", "a"): 0,
      ("b", "b"): 0
    }
    partition_1 = ["a"]
    partition_2 = ["b"]

    result = get_xor_conformance(dfg, partition_1, partition_2)
    self.assertEqual(result, (0.5, 1, 0.6666666666666666))

  def test_get_xor_conformance_v3(self):
    dfg = {
      ("a", "a"): 0,
      ("a", "b"): 0,
      ("b", "a"): 1,
      ("b", "b"): 0
    }
    partition_1 = ["a"]
    partition_2 = ["b"]

    result = get_xor_conformance(dfg, partition_1, partition_2)
    self.assertEqual(result, (0.5, 1, 0.6666666666666666))

  def test_get_and_conformance_v1(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 2, 2, 3, 3],
      "concept:name": ["A", "B", "A", "B", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])

    log_1 = pd.DataFrame({
      "case:concept:name": [1, 2, 3],
      "concept:name": ["A", "A", "A"],
      "time:timestamp": [1, 3, 5]
    })
    log_1["time:timestamp"] = pd.to_datetime(log_1["time:timestamp"])
    log_2 = pd.DataFrame({
      "case:concept:name": [1, 2, 3],
      "concept:name": ["B", "B", "B"],
      "time:timestamp": [2, 4, 6]
    })
    log_2["time:timestamp"] = pd.to_datetime(log_2["time:timestamp"])

    result = get_and_conformance(log, log_1, log_2)
    self.assertEqual(result, (1,0.25,0.4))

  def test_get_and_conformance_v2(self):
    log = pd.DataFrame({
      "case:concept:name": [1, 1, 2, 2, 3, 3],
      "concept:name": ["A", "B", "A", "C", "A", "D"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])

    log_1 = pd.DataFrame({
      "case:concept:name": [1, 2, 3],
      "concept:name": ["A", "A", "A"],
      "time:timestamp": [1, 3, 5]
    })
    log_1["time:timestamp"] = pd.to_datetime(log_1["time:timestamp"])
    log_2 = pd.DataFrame({
      "case:concept:name": [1, 2, 3],
      "concept:name": ["B", "C", "D"],
      "time:timestamp": [2, 4, 6]
    })
    log_2["time:timestamp"] = pd.to_datetime(log_2["time:timestamp"])

    result = get_and_conformance(log, log_1, log_2)
    self.assertEqual(result, (1,0.75, 0.8571428571428571))

  def test_get_loop_conformance_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "2", "2", "2"],
      "concept:name": ["A", "B", "A", "A", "B", "A"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    dfg = {
      ("A", "B"): 2,
      ("B", "A"): 2
    }
    partition_1 = ["A"]
    partition_2 = ["B"]

    loop_a = pd.DataFrame({
      "case:concept:name": ["1", "2", "3", "4"],
      "concept:name": ["A", "A", "A", "A"],
      "time:timestamp": [1, 3, 4, 6]
    })
    loop_a["time:timestamp"] = pd.to_datetime(loop_a["time:timestamp"])

    loop_b = 1
    loop_b = pd.DataFrame({
      "case:concept:name": ["1", "2"],
      "concept:name": ["B", "B"],
      "time:timestamp": [2, 5]
    })
    loop_b["time:timestamp"] = pd.to_datetime(loop_b["time:timestamp"])

    result = get_loop_conformance(log, dfg, partition_1, partition_2, loop_a, loop_b)
    self.assertEqual(result[0], 1)
    self.assertEqual(result[1], 1)
    self.assertEqual(result[2], 1)

  def test_get_loop_conformance_v2(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "2", "2"],
      "concept:name": ["A", "B", "A", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    dfg = {
      ("A", "B"): 1,
      ("B", "A"): 1
    }
    partition_1 = ["A"]
    partition_2 = ["B"]

    loop_a = pd.DataFrame({
      "case:concept:name": ["1", "3", "2"],
      "concept:name": ["A", "A", "A"],
      "time:timestamp": [1, 3, 4]
    })
    loop_a["time:timestamp"] = pd.to_datetime(loop_a["time:timestamp"])

    loop_b = 1
    loop_b = pd.DataFrame({
      "case:concept:name": ["1", "2"],
      "concept:name": ["B", "B"],
      "time:timestamp": [2, 5]
    })
    loop_b["time:timestamp"] = pd.to_datetime(loop_b["time:timestamp"])

    result = get_loop_conformance(log, dfg, partition_1, partition_2, loop_a, loop_b)
    self.assertEqual(result[0], 0.75)
    self.assertEqual(result[1], 0.75)
    self.assertAlmostEqual(result[2], 0.75, places=2)

  def test_get_loop_conformance_v3(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "2", "2", "2"],
      "concept:name": ["A", "B", "A", "C", "D", "C"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    dfg = {
      ("A", "A"): 0,
      ("A", "B"): 1,
      ("A", "C"): 0,
      ("A", "D"): 0,
      ("B", "A"): 1,
      ("B", "B"): 0,
      ("B", "C"): 0,
      ("B", "D"): 0,
      ("C", "A"): 0,
      ("C", "B"): 0,
      ("C", "C"): 0,
      ("C", "D"): 1,
      ("D", "A"): 0,
      ("D", "B"): 0,
      ("D", "C"): 1,
      ("D", "D"): 0
    }
    partition_1 = ["A"]
    partition_2 = ["B"]

    loop_a = pd.DataFrame({
      "case:concept:name": ["1", "2", "3", "4"],
      "concept:name": ["A", "A", "C", "C"],
      "time:timestamp": [1, 3, 4, 6]
    })
    loop_a["time:timestamp"] = pd.to_datetime(loop_a["time:timestamp"])

    loop_b = 1
    loop_b = pd.DataFrame({
      "case:concept:name": ["1", "2"],
      "concept:name": ["B", "D"],
      "time:timestamp": [2, 5]
    })
    loop_b["time:timestamp"] = pd.to_datetime(loop_b["time:timestamp"])

    result = get_loop_conformance(log, dfg, partition_1, partition_2, loop_a, loop_b)
    self.assertEqual(result[0], 1)
    self.assertEqual(result[1], 0.5)
    self.assertAlmostEqual(result[2], 0.6666666666666666, places=2)

  def test_get_tau_loop_confromance_v1(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "1", "1", "1", "2"],
      "concept:name": ["A", "B", "A", "B", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])

    loop_a = pd.DataFrame({
      "case:concept:name": ["1", "1", "2", "2", "3", "3"],
      "concept:name": ["A", "B", "A", "B", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    loop_a["time:timestamp"] = pd.to_datetime(loop_a["time:timestamp"])

    dfg = {
      ("A", "A"): 0,
      ("A", "B"): 3,
      ("B", "A"): 2,
      ("B", "B"): 0
    }

    result = get_tau_loop_confromance(log, dfg, loop_a)
    self.assertEqual(result, (1,1,0.8))

  def test_get_tau_loop_confromance_v2(self):
    log = pd.DataFrame({
      "case:concept:name": ["1", "1", "2", "2", "3", "3"],
      "concept:name": ["A", "B", "D", "C", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])

    loop_a = pd.DataFrame({
      "case:concept:name": ["1", "1", "2", "2", "3", "3"],
      "concept:name": ["A", "B", "D", "C", "A", "B"],
      "time:timestamp": [1, 2, 3, 4, 5, 6]
    })
    loop_a["time:timestamp"] = pd.to_datetime(loop_a["time:timestamp"])

    dfg = {
      ("A", "A"): 0,
      ("A", "B"): 2,
      ("A", "C"): 0,
      ("A", "D"): 0,
      ("B", "A"): 0,
      ("B", "B"): 0,
      ("B", "C"): 0,
      ("B", "D"): 0,
      ("C", "A"): 0,
      ("C", "B"): 0,
      ("C", "C"): 0,
      ("C", "D"): 0,
      ("D", "A"): 0,
      ("D", "B"): 0,
      ("D", "C"): 1,
      ("D", "D"): 0
    }

    result = get_tau_loop_confromance(log, dfg, loop_a)
    self.assertEqual(result, (1, np.float64(0.5), np.float64(0.5333333333333333)))

if __name__ == '__main__':
  unittest.main()