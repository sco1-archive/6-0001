def distances(char, s):
    """
    char, string of length 1
    s, string
    Returns a string detailing the number of characters between 
    successive instances of char. Does not include the number of 
    characters between the start of the string and the first instance 
    of char, or between the last instance of char and the end of the string. 
    If char does not exist in s or it exists only once, returns None
    """
    # Assume char and s are the proper input form, skip error checking

    # Find all indices of char in s
    charidx = []  # Initialize indices
    for idx, letter in enumerate(s):
        if letter == char:
            charidx.append(idx)

    # Check to see if char exists in s at least twice, otherwise return None
    nindices = len(charidx)
    if nindices <= 1:
        return None            
    
    # Loop through and diff the indices
    diffs = ''  # Initialize our diff output
    for idx in range(0, nindices - 1):  # Subtract one so we stay in range
        diffs += str(charidx[idx + 1] - charidx[idx] - 1)  # Append our diff to the output string, subtract 1 to get the proper width

    return diffs

print(distances("a", "bcacabbbaa"))
print(distances("a", "aabbabcd"))
print(distances("a", "bbabcd"))