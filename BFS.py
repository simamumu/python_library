from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,datetime
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inpl(): return list(map(int, input().split()))
def inpl_s(): return list(input().split())

H,W = inpl()
sx,sy = #inpl() #1index
gx,gy = #inpl() #1index

MAP = [['#']*(W+2)]
for i in range(H):
	MAP.append(['#'] + list(input()) + ['#'])
MAP.append(['#']*(W+2))

def check(x,y,n):
	global q
	if x == gx and y == gy:
		#'hoge'
		sys.exit()
	elif MAP[y][x] == '.':
		MAP[y][x] = n
		q.put([x-1,y,n+1])
		q.put([x+1,y,n+1])
		q.put([x,y-1,n+1])
		q.put([x,y+1,n+1])
	else:
		return

q = queue.Queue()
q.put([sx,sy,0])
while not q.empty():
	x,y,n = q.get()
	check(x,y,n)

#hogehoge
