from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,copy,time
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(): return int(sys.stdin.readline())
def inpl(): return list(map(int, sys.stdin.readline().split()))
def inpl_str(): return list(sys.stdin.readline().split())

class Node:
    def __init__(self,value,index):
        self.value = value
        self.index = index

    def __str__(self):
        return 'val : ' + str(self.value) + ' index : ' + str(self.index)

# 0-indexed SegmentTree
class SegmentTree:
    def __init__(self,N,default_list,default_value=INF):
        self.N0 = pow(2,(N-1).bit_length())
        self.nodes = [Node(default_value,i+1-self.N0) for i in range(2*self.N0-1)]
        for i in reversed(range(2*self.N0-1)):
            ind = i+1-self.N0
            if ind >= N:
                self.nodes[i].value = default_value
            elif N > ind >= 0:
                self.nodes[i].value = default_list[ind]
            else:
                self.nodes[i] = self.process(self.nodes[i*2+1],self.nodes[i*2+2])

    def __getitem__(self,key): # getiten : ST[i]
        return self.nodes[key+self.N0-1].value

    def __setitem__(self,i,x): # update : ST[i] = x
        i += self.N0 - 1
        self.nodes[i].value = x
        while i > 0:
            i = (i-1)//2
            self.nodes[i] = self.process(self.nodes[i*2+1],self.nodes[i*2+2])

    def __str__(self):
        return '['+', '.join(map(str,[self.nodes[i+self.N0-1].value for i in range(self.N0)]))+']'

    def query(self,L,R): #[L,R)の値
        retnode = Node(INF,INF)
        L += self.N0
        R += self.N0
        while L < R:
            if R&1 :
                R -= 1
                retnode = self.process(retnode,self.nodes[R-1])
            if L&1 :
                retnode = self.process(retnode,self.nodes[L-1])
                L += 1
            L >>= 1; R >>= 1
        return retnode

    def process(self,node_x,node_y): #x,yが子の時，親に返る値
        if node_x.value < node_y.value:
            return node_x
        else:
            return node_y

N,Q = inpl()
ST = SegmentTree(N,inpl())
for _ in range(Q):
    q,l,r = inpl()
    if q == 1:
        ST[l-1],ST[r-1] = ST[r-1],ST[l-1]
    else:
        print(ST.query(l-1,r).index+1)
