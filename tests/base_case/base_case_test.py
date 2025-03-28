import unittest
import pandas as pd
from optimiist.base_case.base_case import get_base_case
from pm4py.objects.process_tree.obj import ProcessTree

class TestGetBaseCase(unittest.TestCase):

  def setUp(self):
    self.empty_log = pd.DataFrame(columns=["case:concept:name", "concept:name"])
    self.single_activity_log = pd.DataFrame({
      "case:concept:name": [1],
      "concept:name": ["A"]
    })
    self.multi_activity_log = pd.DataFrame({
      "case:concept:name": [1, 2],
      "concept:name": ["A", "B"]
    })
    self.multi_activity_log_2 = pd.DataFrame({
      "case:concept:name": [1, 2, 3],
      "concept:name": ["A", "A", "A"]
    })
    self.multi_activity_log_3 = pd.DataFrame({
      "case:concept:name": [1, 1, 2],
      "concept:name": ["A", "A", "A"]
    })

  def test_empty_log(self):
    result = get_base_case(self.empty_log)
    self.assertIsInstance(result, ProcessTree)
    self.assertIsNone(result.label)
    self.assertEqual(len(result.children), 0)

  def test_single_activity_log(self):
    result = get_base_case(self.single_activity_log)
    self.assertIsInstance(result, ProcessTree)
    self.assertEqual(result.label, "A")
    self.assertEqual(len(result.children), 0)

  def test_multi_activity_log(self):
    result = get_base_case(self.multi_activity_log)
    self.assertIsNone(result)

  def test_multi_activity_log_2(self):
    result = get_base_case(self.multi_activity_log_2)
    self.assertIsInstance(result, ProcessTree)
    self.assertEqual(result.label, "A")
    self.assertEqual(len(result.children), 0)

  def test_multi_activity_log_3(self):
    result = get_base_case(self.multi_activity_log_3)
    self.assertIsInstance(result, ProcessTree)
    self.assertEqual(str(result.operator), "*")
    self.assertEqual(len(result.children), 2)
    # No empty traces so first child A
    self.assertEqual(result.children[0].label, "A")
    # Second child empty
    self.assertIsNone(result.children[1].label)

if __name__ == '__main__':
  unittest.main()