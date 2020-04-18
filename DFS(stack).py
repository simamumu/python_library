from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,copy,time
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(): return int(sys.stdin.readline())
def inpl(): return list(map(int, sys.stdin.readline().split()))
def inpl_str(): return list(sys.stdin.readline().split())

N,M = inpl()

if M == N-1: # 一本道
    for _ in range(M):
        s,t = inpl()
    print(M)
else:
    lines = defaultdict(set)
    LL = [0]*N
    for _ in range(M):
        s,t = inpl()
        s -= 1; t -= 1
        lines[s].add(t)
        LL[s] += 1


    def dfs(s):
        global MEMO
        if MEMO[s] != -1:
            return MEMO[s]
        else:
            tmp = 0
            for t in lines[s]:
                tmp += dfs(t) + 1
            L = len(lines[s])
            MEMO[s] = tmp / LL[s]
            return MEMO[s]

    ans = 10**10
    for s in range(N-1):
        for t in lines[s]:
            if LL[s] == 1:
                continue
            MEMO = [-1]*N
            MEMO[-1] = 0
            lines[s].remove(t)
            LL[s] -= 1
            tmp = dfs(0)
            #print(s,t,tmp)
            ans = min(ans,tmp)
            lines[s].add(t)
            LL[s] += 1
    print(ans)
