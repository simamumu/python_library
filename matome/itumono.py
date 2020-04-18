
###### ICPC用スニペット ######

from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(f): return int(f.readline())
def inps(f): return f.readline().rstrip()
def inpl(f): return list(map(int, f.readline().split()))
def inpls(f): return list(f.readline().split())

inpf = open('A.dat')
outf = open('Aout.dat',mode='w')

while True:
    x = inp(inpf)
    if x == 0:
        break

    outf.write('nya-n\n')
