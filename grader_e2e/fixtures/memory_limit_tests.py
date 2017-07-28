import unittest
from solution import sum_of_numbers


class TestStringMethods(unittest.TestCase):
    def test_sum_of_zero(self):
        self.assertEqual(sum_of_numbers(0), 0)

    def test_sum_of_ten(self):
        self.assertEqual(sum_of_numbers(10), 1)

    def test_sum_of_one_hundred(self):
        self.assertEqual(sum_of_numbers(100), 1)


if __name__ == '__main__':
    unittest.main()
