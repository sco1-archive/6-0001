# Problem Set 4A
# Name: sco1
# Collaborators:
# Time Spent: 0:30

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # Per the docstring, assume input is proper form so we only have 2 edge 
    # cases: zero and one length strings
    if len(sequence) <= 1:
        # Short circuit for the edge cases
        return [sequence]
    
    outstrs = []  # Initialize output
    # Iterate over our string and recurse to build up the permutations
    for letter in sequence:
        # Only replace 1 character so we don't ignore duplicate letters
        perms = get_permutations(sequence.replace(letter, '', 1))

        # Go through the recursed permutations and append our build character 
        # (letter) to them
        for perm in perms:
            newperm = letter + perm
            # Check for duplicates, only append if it's a unique value in the 
            # output list
            if outstrs.count(newperm) == 0:
                outstrs.append(letter + perm)

    return outstrs


if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # Test a 'standard' input
    input1 = 'abc'
    print('Input:', input1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(input1))

    # Test repeat character case
    input2 = 'aab'
    print('Input:', input2)
    print('Expected Output:', ['aab', 'aba', 'baa'])
    print('Actual Output:', get_permutations(input2))

    input3 = 'aa'
    print('Input:', input2)
    print('Expected Output:', ['aa'])
    print('Actual Output:', get_permutations(input3))

    # Test the single character edge case
    input4 = 'a'
    print('Input:', input4)
    print('Expected Output:', ['a'])
    print('Actual Output:', get_permutations(input4))