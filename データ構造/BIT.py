
class BinaryIndexedTree():
    def __init__(self,N):
        self.N = N
        self.bit = [0]*(self.N+1)

    def add(self,a,w):
        x = a
        while x <= self.N:
            self.bit[x] += w
            x += x & -x

    def sum(self,a):
        tmp = 0
        x = a
        while x > 0:
            tmp += self.bit[x]
            x -= x & -x
        return tmp
