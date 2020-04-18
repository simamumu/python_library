from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,datetime
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(): return int(input())
def inpl(): return list(map(int, input().split()))
def inpls(): return list(input().split())

S1 = 'yafo'
S2 = 'yahoo'

def levenshtein(s1,s2):
    n, m = len(s1), len(s2)
    dp = [[0]*(m+1) for _ in range(n + 1)]

    for i in range(n+1):dp[i][0] = i
    for j in range(m+1):dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:cost = 0
            else:cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1,         # insertion
                           dp[i][j - 1] + 1,         # deletion
                           dp[i - 1][j - 1] + cost)  # replacement
    return dp[n][m]

print(levenshtein(S1,S2))
