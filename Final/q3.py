class myDict(object):
    """ Implements a dictionary without using a dictionary """
    def __init__(self):
        """ initialization of your representation """
        self.keys = []
        self.values = []
        
    def assign(self, k, v):
        """ k (the key) and v (the value), immutable objects  """
        if k not in self.keys:
            self.keys.append(k.copy())
            self.values.append(v.copy())
        else:
            idx = self.keys.index(k)
            self.values.idx = v.copy()
        
    def getval(self, k):
        """ k, immutable object  """
        if k in self.keys:
            idx = self.keys.index(k)
            return self.values[idx]
        else:
            raise KeyError
        
    def delete(self, k):
        """ k, immutable object """   
        if k in self.keys:
            idx = self.keys.index(k)
            self.keys.pop(idx)
            self.values.pop(idx)
        else:
            raise KeyError

md = myDict()
md.assign(1, 2)
md.assign('1', 3)
print(md.getval(1))
md.delete(1)
print(md.getval('1'))