import unittest

from lib import (
    Assignment,
    Course,
    Grade,
    calculate_bsc,
    calculate_msci,
    calculate_placement,
)


class TestCalculationsBsc(unittest.TestCase):
    def test_gethin(self):
        l3 = [
            Assignment("TP", 30, Grade["B1"], True),
            Assignment("1E", 8, Grade["A5"], False),
            Assignment("1C", 2, Grade["B2"], False),
            Assignment("2E", 8, Grade["A3"], False),
            Assignment("2C", 2, Grade["A3"], False),
            Assignment("3E", 8, Grade["B2"], True),
            Assignment("3C", 2, Grade["A5"], False),
            Assignment("4E", 8, Grade["C1"], True),
            Assignment("4C", 2, Grade["A2"], False),
            Assignment("5E", 8, Grade["A5"], True),
            Assignment("5C", 2, Grade["A1"], True),
            Assignment("6E", 8, Grade["B2"], True),
            Assignment("6C", 2, Grade["A3"], True),
            Assignment("7E", 8, Grade["C3"], True),
            Assignment("7C", 2, Grade["C2"], True),
            Assignment("8E", 8, Grade["A5"], True),
            Assignment("8C", 2, Grade["B1"], True),
            Assignment("9E", 8, Grade["B1"], True),
            Assignment("9C", 2, Grade["C3"], True),
        ]
        l4 = [
            Course("IP", 40, Grade["B2"]),
            Course("1", 10, Grade["B1"]),
            Course("2", 10, Grade["A4"]),
            Course("3", 10, Grade["B3"]),
            Course("4", 10, Grade["B2"]),
            Course("5", 10, Grade["A3"]),
            Course("6", 10, Grade["A5"]),
            Course("7", 10, Grade["B1"]),
            Course("8", 10, Grade["A5"]),
        ]
        result = calculate_bsc(l3, l4)
        self.assertAlmostEqual(result.baseline_gpa, 17.2, 1)
        self.assertAlmostEqual(result.final_gpa, 17.3, 1)
        self.assertAlmostEqual(result.credits_used_unweighted, 8 + 2 + 2 + 8 + 144, 1)
        self.assertEqual(len(result.excluded_assignments), 13 - 4)

    def test_empty(self):
        with self.assertRaises(AssertionError):
            calculate_bsc([], [])

    def test_partial_credits(self):
        l4 = [
            Course("IP", 40, Grade["H0"]),
            Course("1", 10, Grade["H0"]),
            Course("2", 10, Grade["H0"]),
            Course("3", 10, Grade["H0"]),
            Course("4", 10, Grade["H0"]),
            Course("5", 10, Grade["H0"]),
            Course("6", 10, Grade["H0"]),
            Course("7", 10, Grade["H0"]),
            Course("8", 10, Grade["H0"]),
        ]
        result = calculate_bsc([], l4)
        self.assertEqual(result.credits_used_unweighted, 120)
        self.assertEqual(result.credits_unused_unweighted, 0)

    def test_overexclusion(self):
        l3 = [
            Assignment("X", 100, Grade["H0"], True),
            Assignment("Y", 20, Grade["A1"], True),
        ]
        l4 = [
            Course("IP", 40, Grade["B2"]),
            Course("1", 10, Grade["B1"]),
            Course("2", 10, Grade["A4"]),
            Course("3", 10, Grade["B3"]),
            Course("4", 10, Grade["B2"]),
            Course("5", 10, Grade["A3"]),
            Course("6", 10, Grade["A5"]),
            Course("7", 10, Grade["B1"]),
            Course("8", 10, Grade["A5"]),
        ]
        result = calculate_bsc(l3, l4)
        self.assertEqual(result.credits_used_unweighted, 140)
        self.assertEqual(result.credits_unused_unweighted, 100)


class TestCalculationsPlacement(unittest.TestCase):
    def test_weighs(self):
        l3 = [Assignment("X", 120, Grade["A1"], True)]
        l4 = [Course("X", 120, Grade["A1"])]
        l5 = [Course("X", 120, Grade["B1"])]
        result = calculate_placement(l3, l4, l5)
        self.assertEqual(result.final_gpa, 19.5)
        self.assertEqual(result.baseline_gpa, 18.4)


class TestCalculationsMsci(unittest.TestCase):
    def test_weighs(self):
        l3 = [Assignment("X", 120, Grade["A1"], True)]
        l4 = [Course("X", 120, Grade["A1"])]
        l5 = [Course("X", 120, Grade["B1"])]
        result = calculate_msci(l3, l4, l5)
        self.assertEqual(result.final_gpa, 20)
        self.assertEqual(result.baseline_gpa, 19.4)


if __name__ == "__main__":
    unittest.main()
