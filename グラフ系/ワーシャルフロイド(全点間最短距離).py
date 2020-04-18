from collections import defaultdict
import sys,heapq,bisect,math,itertools,string,queue,datetime
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inpl(): return list(map(int, input().split()))
def inpl_s(): return list(input().split())


N = inp()

for _ in range(N):
	a,b = inpl()
	a,b = a-1,b-1
	cost[a][b] = 1
	cost[b][a] = 1


for k in range(N):
	for i in range(N):
		for j in range(N):
			cost[i][j]=min(cost[i][j],cost[i][k]+cost[k][j])


ans = 0
for a in range(N):
	for b in range(N):
		ans += cost[a][b]**2
		ans %= mod

print(ans)
