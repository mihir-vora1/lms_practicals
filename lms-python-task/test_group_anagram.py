import unittest
from group_anagram import Anagrams

class TestGroupingAnagrams(unittest.TestCase):
	def test_group_anagram_valid(self):
		"""
		Valid Test Cases
		"""
		# Test Case 1
		strs = ["eat","tea","tan","ate","nat","bat"]
		expected_output = [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
		self.assertEqual(Anagrams().group_anagram(strs), expected_output)
		print("Test Case 1 Passed")

		strs = [""]
		expected_output = [[""]]
		self.assertEqual(Anagrams().group_anagram(strs), expected_output)
		print("Test Case 2 Passed")

		strs = ["a", "b"]
		expected_output = [["a"], ["b"]]
		self.assertEqual(Anagrams().group_anagram(strs), expected_output)
		print("Test Case 3 Passed")

		

if __name__ == '__main__':
	unittest.main()