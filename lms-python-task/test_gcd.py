import unittest
from gcd import GCD


class TestGCD(unittest.TestCase):
    def test_valid_input(self):
        # Test Case 1
        expected_output = 'onezero'
        self.assertEqual(GCD('onezero', 'twozero').compute_gcd(), expected_output)
        print("Test Case 1 Passed")

        # Test Case 2
        expected_output = 'two'
        self.assertEqual(GCD('twosix', 'twofour').compute_gcd(), expected_output)
        print("Test Case 2 Passed")

        # Test Case 3
        expected_output = 'one'
        self.assertEqual(GCD('fourfivesixseven', 'ninezeroone').compute_gcd(), expected_output)
        print("Test Case 3 Passed")

        # Test Case 4
        expected_output = 'onefour'
        self.assertEqual(GCD('nineeight', 'fivesix').compute_gcd(), expected_output)
        print("Test Case 4 Passed")

        # Test Case 5
        expected_output = 'threesix'
        self.assertEqual(GCD('onezeroeight', 'onefourfour').compute_gcd(), expected_output)
        print("Test Case 5 Passed")


if __name__ == '__main__':
    unittest.main()