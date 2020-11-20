import os
import unittest
from evaluator.data.standard_reader import StandardReader


class TestStandardReader(unittest.TestCase):

    def test_standard_reader(self):
        path = os.path.join(os.path.dirname(__file__), "../_data/standard_example.xlsx")
        reader = StandardReader()
        standards = reader.read(path, "TCFD", skiprows=3)
        self.assertEqual(len(standards.standard_items), 11)
