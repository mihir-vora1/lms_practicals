import unittest
from generate_well_formed_parentheses import GenerateWellFormedParentheses

class TestGenerateWellFormedParentheses(unittest.TestCase):
	def test_generate_parentheses(self):
		# Test Case 1
		num = 0
		expected_output = []
		self.assertEqual(
					GenerateWellFormedParentheses().generate_parentheses(num), 
					expected_output
				)
		print("Test Case 1 Passed")

		# Test Case 2
		num = 1
		expected_output = ["()"]
		self.assertEqual(
					GenerateWellFormedParentheses().generate_parentheses(num), 
					expected_output
				)
		print("Test Case 2 Passed")

		# Test Case 3
		num = 3
		expected_output = ['()()()', '(()())', '()(())', '((()))', '(())()']
		expected_output.sort()
		self.assertEqual(
					sorted(GenerateWellFormedParentheses().generate_parentheses(num)), 
					expected_output
				)
		print("Test Case 3 Passed")

		# Test Case 4
		num = 4
		expected_output = ['()(())()', '()((()))', '((())())', '()(()())', '((()))()', '()()(())', '(())(())', '()()()()', '(())()()', '((()()))', '(()()())', '(((())))', '(()(()))', '(()())()']
		expected_output.sort()
		self.assertEqual(
					sorted(GenerateWellFormedParentheses().generate_parentheses(num)), 
					expected_output
				)
		print("Test Case 4 Passed")

if __name__ == '__main__':
	unittest.main()