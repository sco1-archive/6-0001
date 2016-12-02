def max_odd(L):
    """
    L, non-empty list of positive integers
    Returns the largest odd number in L. 
    If there is no odd number, returns None
    """
    # Assume L is the proper input form, skip error checking
    L.sort()  # Sort L smallest to largest
    nelements = len(L)  # Get number of elements in L
    
    # Start at the end and work backwards, look for where L mod 2 != 0
    for idx in range((nelements - 1), -1, -1):  # Subtract 1 from our start so we don't go out of range
        if L[idx] % 2 != 0:
            return L[idx]
    else:
        # If we get here we never found an odd number, return None
        return None

print(max_odd([3, 4, 5, 6]))
print(max_odd([4, 6, 8]))
print(max_odd([6, 3, 1, 5]))