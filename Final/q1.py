def gcd(a, b):
    """
    a, b: two positive integers
    Returns the greatest common divisor of a and b
    """
    # Skipping any input validation

    # Force a >= b
    tmp = [a, b]
    tmp.sort()
    a1 = tmp[0]
    b1 = tmp[1]

    # Ugly version because I couldn't figure out the recursion in time
    test = a1 % b1
    while test != 0:
        test = a1 % b1
        if test != 0:
            a1 = b1
            b1 = test
    
    return b1


print(gcd(12, 20))
print(gcd(20, 12))
print(gcd(15, 5))
print(gcd(20, 10))
print(gcd(13, 3))
print(gcd(3, 13))