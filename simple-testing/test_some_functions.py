import unittest
from add import add


class TestAdd(unittest.TestCase):
    def test_returns_numbers(self):
        """The add function should return a number"""
        self.assertIsInstance(
            add(1, 2),
            (int, float),
            f"Add function is supposed to return int or float, but returned {add(1, 2)}, and instance of {type(add(1, 2))}",
        )

    def test_works_with_ints(self):
        """The add function should work with ints"""
        self.assertEqual(add(1, 2), 3, f"It said 1 + 2 != 3 :(")
        self.assertEqual(add(-2, 2), 0, f"It said -2 + 2 != 0 :(")

    def test_works_with_floats(self):
        """The add function should work with floats"""
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)
        self.assertAlmostEqual(add(-0.2, 2), 1.8)

    def test_fails_on_non_numbers(self):
        """The add function should fail on anything else"""
        bad_values = [["1", "2"], [{"bad": "value"}, []]]

        for [first, second] in bad_values:
            with self.assertRaises(TypeError):
                add(first, second)
