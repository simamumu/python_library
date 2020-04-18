from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,copy,time
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(): return int(input())
def inpl(): return list(map(int, input().split()))
def inpl_str(): return list(input().split())

N,M = inpl()
lines = defaultdict(set)
hh = [0]*N
for _ in range(M):
    x,y = inpl()
    lines[x].add(y)
    hh[y] += 1

def TopologicalSort(N,lines,hh):
    q = queue.Queue()
    for t in range(N):
        if hh[t] == 0:
            q.put(t)

    topological = []
    while not q.empty():
        s = q.get()
        topological.append(s)
        for t in lines[s]:
            hh[t] -= 1
            if hh[t] == 0:
                q.put(t)

    return topological
