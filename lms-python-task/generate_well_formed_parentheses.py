"""
Given n pairs of parentheses, write a function to generate all 
combinations of well-formed parentheses.
"""


class GenerateWellFormedParentheses:
    """
    generate all combination of parentheses
    """

    def generate_parentheses(self, num: int):
        """
        generate all valid combinations of n pairs of parentheses
        """

        # base case
        # check if num is 0, return empty list
        if num <= 0:
            return []
        if num >= 9:
            return "Pls, Enter number below or eqaul to 8"

        # create list with first element as '()'
        result = ["()"]

        # Iterate from 2 to num+1
        for _ in range(2, num + 1):
            # create new empty set to store the unique results
            new_result = set()
            # Iterate over the each string of the result input string
            for result_ele in result:
                # Iterate over the each character of string
                for index_j in range(len(result_ele)):
                    new_result.add(
                        result_ele[: index_j + 1] + "()" + result_ele[index_j + 1 :]
                    )
                # Insert the start of the String
                new_result.add("()" + result_ele)
            # convert the set to list and update the result
            result = list(new_result)
        return result


if __name__ == "__main__":
    generate_parenthesis_obj = GenerateWellFormedParentheses()
    user_input = int(input("Enter the Number: "))
    output = generate_parenthesis_obj.generate_parentheses(user_input)
    print(output)
