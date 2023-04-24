"""
Write a program for computing GCD of 2 numbers with optimal data structures and less time-consuming.
"""
import sys

class GCD:
    """
    class for computing GCD of two intergers number using Euclidean algorithm
    """

    def __init__(self, num1: str, num2: str) -> str:
        """
        initialize the GCD object with two integer num1 and num2
        """
        self.num1 = num1
        self.num2 = num2

    def compute_gcd(self):
        """
        compute the GCD of two integer numbers num1 and num2
        """
        words_to_num_dict = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
		# calling the str_to_number function that return integer number of given words input
		# handling the error ( if input is integer and negative value )
        try:
            str_to_num1 = self.str_to_number(self.num1, words_to_num_dict)
            str_to_num2 = self.str_to_number(self.num2, words_to_num_dict)
        except ValueError:
            return "Please enter the proper value (integer number and negative number not allowed)"

        # base Case
        if str_to_num1 == 0:
            return str_to_num1
        if str_to_num2 == 0:
            return str_to_num2

        # calculation of GCD of two numbers using while loop
        while str_to_num1 != str_to_num2:
            if str_to_num1 > str_to_num2:
                str_to_num1 = str_to_num1 - str_to_num2
            else:
                str_to_num2 = str_to_num2 - str_to_num1
        return self.number_to_str(str(str_to_num1), words_to_num_dict)

    def str_to_number(self, words: str, words_to_num_dict):
        """
        function convert the input str to interger number and return result of integer
        """
        result = ""
        append_word_characters = ""
        words_len = len(words)
        count = 0
        while words_len > 0:
            append_word_characters += words[count]
            if append_word_characters in words_to_num_dict:
                result += str(words_to_num_dict[append_word_characters])
                append_word_characters = ""
            words_len -= 1
            count += 1
        return int(result)

    def number_to_str(self, nums, words_to_num_dict):
        """
        Convert the Number To String and return final word number String
        """
        result = ""
        concat_str_char = ""
        outer_counter = 0
        int_len = len(nums)
        while int_len > 0:
            concat_str_char += nums[outer_counter]
            if int(concat_str_char) in words_to_num_dict.values():
                itm = list(words_to_num_dict.items())
                len_itm = len(itm)
                inner_counter = 0
                under_count = 0
                while len_itm > 0:
                    if int(itm[inner_counter][1]) == int(concat_str_char):
                        result += str(itm[inner_counter][0])
                    inner_counter += 1
                    under_count += 1
                    len_itm -= 1
            concat_str_char = ""
            int_len -= 1
            outer_counter += 1
        return result


if __name__ == "__main__":
    if len(sys.argv) < 4:
        gcd = GCD(sys.argv[1], sys.argv[2])
        print(f"GCD of the {sys.argv[1]} and {sys.argv[2]} number: {gcd.compute_gcd()}")
    else:
        print("Error: Enter Only Number in words")



