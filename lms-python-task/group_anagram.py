"""
Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, 
typically using all the original letters exactly once.
"""

class Anagrams:
    """
    Given an array of strings strs, group the anagrams together
    """

    def group_anagram(self, strs):
        """
        groups anagram function take the list and return group of anagrams together
        """
        # Base Cases
        if not 1 <= len(strs) <= 104:
            return "Length of the List must in between 1 and 104"

        for value in strs:
            if not 0 <= len(value) <= 100:
                return "Length of Each String Item must be in between 0 and 100"

            if not (value.islower() if len(value) != 0 else True):
                return "List item must be a Lower Case"

        # create dictionary to store the group of anagrams
        groups = {}

        # Iterate over each string of the input list
        for str_element in strs:
            # sort the characters of string to create unique key
            key = "".join(sorted(str_element))
            # Check key already present or not in group dictionary
            # if not present create key in group and assign empty list to that key
            if key not in groups:
                groups[key] = []

            # Add the string to the corresponding group based on the key
            groups[key].append(str_element)

        # returns the list of anagram groups
        return list(groups.values())


if __name__ == "__main__":
    # create object of Anagram class
    anagram = Anagrams()
    usr_input = []
    for i in range(int(input("Enter the length of list words: "))):
        usr_input.append(input("Enter the Anagrams Words: "))
    # group_anagram_list =  ["eat","tea","tan","ate","nat","bat"]
    result = anagram.group_anagram(usr_input)
    print(result)
