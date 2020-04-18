from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,copy,time
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(): return int(input())
def inpl(): return list(map(int, input().split()))
def inpl_str(): return list(input().split())

class Tree:
    def __init__(self,N):
        self.inlines = defaultdict(set)
        #self.lines = defaultdict(set)
        self.depth = [-1]*N
        self.parents = [[-1]*int(math.log2(N)+1) for _ in range(N)]

    def add_edge(self,x,y,c=1):
        self.inlines[x].add((y,c))
        self.inlines[y].add((x,c))

    def build(self):
        visited = [False]*N
        def dfs(s,pp,d):
            visited[s] = True
            self.depth[s] = d
            i,j = 1,0
            while i <= d:
                self.parents[s][j] = pp[d-i]
                i,j = i*2,j+1
            for t,c in self.inlines[s]:
                if not visited[t]:
                    #self.lines[s].add((t,c))
                    dfs(t,pp+[s],d+1)
        dfs(0,[],0)

    def up(self,x,n): # x の n個上 O(logN)
        L = n.bit_length()
        for b in range(L):
            if n & (1<<b):
                x = self.parents[x][b]
        return x

    def lca(self,x,y): # x,y の 最深共通祖先
        dx,dy = self.depth[x],self.depth[y]
        d = min(dx,dy)
        x,y = self.up(x,dx-d),self.up(y,dy-d) #深さを合わせる
        if x == y:
            return x
        else:
            NG = 0
            OK = d
            while OK-NG > 1:
                mid = (OK+NG)//2
                if self.up(x,mid) == self.up(y,mid):
                    OK = mid
                else:
                    NG = mid
            return self.up(x,OK)

N = inp()
tree = Tree(N)
for s in range(N):
    arg = inpl()
    first = True
    for t in arg:
        if first:
            first = False
            continue
        else:
            tree.add_edge(s,t)

tree.build()

q = inp()
for _ in range(q):
    x,y = inpl()
    print(tree.lca(x,y))
