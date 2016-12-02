def lengths(L):
    """
    L, non-empty list of strings and ints
    Returns a list where its elements are:
        the length of the string, if the element in L is a string
        the number of digits in the integer, if the element in L is an int
    """
    # Assume L is the proper input form, skip error checking

    output = []  # Initialize our output
    for item in L:
        # Iterate over L, cast the entry as a string and count the elements
        itemStr = str(item)
        itemStr = itemStr.replace('-', '')  # Strip out negative sign
        output.append(len(itemStr))
    
    return output

print(lengths(['a', 'abcd', 'ab', 34]))
print(lengths(['a', 'abcd', 'ab', -34]))