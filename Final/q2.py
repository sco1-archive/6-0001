def unique_values(aDict):
    '''
    aDict: a dictionary that maps ints to strings
    Returns a sorted list of the keys that map to unique aDict values, empty list if no keys
    '''
    # Skipping input validation
    outkeys = []
    for key in aDict.keys():
        for searchkey in aDict.keys():
            if searchkey == key:
                continue
            if aDict[searchkey] == aDict[key]:
                break
        else:
            outkeys.append(key)    
    outkeys.sort()

    return outkeys

print(unique_values({1:'a', 2:'b', 3:'c', 4:'c', 5:'d'}))
print(unique_values({1:'a', 2:'a', 3:'a'}))