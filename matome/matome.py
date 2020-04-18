########################
#       itsumono       #
########################
from collections import defaultdict,deque
import sys,heapq,bisect,math,itertools,string,queue,copy,time
sys.setrecursionlimit(10**8)
INF = float('inf')
mod = 10**9+7
eps = 10**-7
def inp(): return int(input())
def inpl(): return list(map(int, input().split()))
def inpl_str(): return list(input().split())



########################
#         graph        #
########################

def dijkstra(lines,N,s):
    weight = [INF]*N
    weight[s] = 0

    def search(s,w_0,q,weight):
        for t,w in lines[s]:
            w += w_0
            if weight[t] > w:
                heapq.heappush(q,[w,t])
                weight[t] = w

    q = [[0,s]]
    heapq.heapify(q)
    while q:
        w,n = heapq.heappop(q)
        search(n,w,q,weight)

    return weight


def BellmanFord(Start,Goal):
	Costs=[INF]*N
	Costs[Start] = 0
	upd8s = [True]*N
	for i in range(2*N): #2N回ループ(負回路の検出までみる)
		will_upd8s = [False]*N
		upd8 = False
		for s in range(N):
			if not upd8s[s]: continue	#前回更新してないので見ない
			for t,c in lines[s]:
				if c + Costs[s] < Costs[t]:
					Costs[t] = Costs[s]+c
					upd8 = True
					will_upd8s[t] = True #更新した点だけ次に見る

		if not upd8: #なにも更新しなかったら終わり
			return Costs[Goal]

		if i == N-1: #Nループ目のGoalのCostを記録
			tmp = Costs[Goal]

		upd8s = will_upd8s[:]

	if tmp != Costs[Goal]:
		return -INF
	else:
		return Costs[Goal]

print(-BellmanFord(0,N-1))


def FordFulkerson(S,T): #sからFord-Fulkerson
    global lines
    global cost
    global ans

    queue = deque()     #BFS用のdeque
    queue.append([S,INF])
    ed = [True]*N    #到達済み
    ed[S] = False
    route = [0 for i in range(N)]   #ルート
    route[S] = -1

    #BFS
    while queue:
        s,flow = queue.pop()
        for t in lines[s]:  #s->t
            if ed[t]:
                flow = min(cost[s][t],flow)  #flow = min(直前のflow,line容量)
                route[t] = s
                queue.append([t,flow])
                ed[t] = False
                if t == T: #ゴール到達
                    ans += flow
                    break
        else:
            continue
        break
    else:
        return False

    #ラインの更新
    t = T
    s = route[t]
    while s != -1:
        #s->tのコスト減少，ゼロになるなら辺を削除
        cost[s][t] -= flow
        if cost[s][t] == 0:
            lines[s].remove(t)

        #t->s(逆順)のコスト増加，元がゼロなら辺を作成
        if cost[t][s] == 0:
            lines[t].add(s)
        cost[t][s] += flow

        t = s
        s = route[t]
    return True

while FordFulkerson(S,T):
    pass


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


# 最小全域木
def Prim(N,M):
    UF = UnionFind(N)
    q = []
    for i in range(M):
    	a,b,w = inpl()
    	a,b = a-1,b-1
    	q.append([w,a,b])

    q.sort()
    weight = 0

    for w,a,b in q:
    	if not UF.Check(a,b):
    		weight += w
    		UF.Unite(a,b)

    return weight

# ワーシャルフロイド
for _ in range(M):
	a,b,c = inpl()
	a,b = a-1,b-1
	cost[a][b] = c
	cost[b][a] = c

for k in range(N):
	for i in range(N):
		for j in range(N):
			cost[i][j]=min(cost[i][j],cost[i][k]+cost[k][j])

# LCA
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




########################
#      data ko-zo      #
########################
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

#
class UnionFind:
    def __init__(self,N): # 頂点数 N
        self.table = [i for i in range(N)]    # 親 table[x] == x で根
        self.rank  = [1 for i in range(N)]    # 木の長さ
        self.size  = [1 for i in range(N)]    # 集合のサイズ

    def Find(self,x):    #xの根を返す
        if self.table[x] == x:
            return x
        else:
            self.table[x] = self.Find(self.table[x]) #親の更新
            self.size[x] = self.size[self.table[x]]
            return table[x]

    def Unite(self,x,y,w): #xとyをdiff(x,y)=W で繋げる
        w = w - self.weight(y) + self.weight(x)
        x,y = self.Find(x), self.Find(y)
        sx,sy = self.Size(x), self.Size(y)
        if x == y: return
        if self.rank[x] > self.rank[y]:
            self.table[y] = x
            self.size[x] = sx + sy
        else:
            self.table[x] = y
            self.size[y] = sx + sy
            if self.rank[x] == self.rank[y]:
                self.rank[y] += 1

    def Check(self,x,y):
        return self.Find(x) == self.Find(y)

    def Size(self,x):
        return self.size[self.Find(x)]

#
class SegmentTree:
    def __init__(self,N,d):
        self.NN = 1
        while self.NN < N:
            self.NN *= 2
        self.SegTree = [d]*(self.NN*2-1)

    def update(self,i,x): #iの値をxに更新
        i += self.NN - 1
        self.SegTree[i] = x
        while i>0:
            i = (i-1)//2
            self.SegTree[i] = self.process(self.SegTree[i*2+1],self.SegTree[i*2+2])

    def query(self,a,b,k=0,l=0,r=None): #[A,B)の値, 呼ぶときはquery(a,b)
        if r == None: r = self.NN
        if r <= a or b <= l: #完全に含まない
            return INF
        elif a <= l and r <= b : #完全に含む
            return self.SegTree[k]
        else: #交差する
            vl = self.query(a,b,k*2+1,l,(l+r)//2)
            vr = self.query(a,b,k*2+2,(l+r)//2,r)
            return(self.process(vl,vr))

    def process(self,x,y): #x,yが子の時，親に返る値
        return min(x,y)

#
class PotentialUnionFind:
    def __init__(self,N): # 頂点数 N
        self.table = [i for i in range(N)]    # 親 table[x] == x で根
        self.rank  = [1 for i in range(N)]    # 木の長さ
        self.size  = [1 for i in range(N)]    # 集合のサイズ
        self.diffweight = [0 for i in range(N)]

    def Find(self,x):    #xの根を返す
        if self.table[x] == x:
            return x
        else:
            root = self.Find(self.table[x]) #親の更新
            self.size[x] = self.size[self.table[x]]
            self.diffweight[x] += self.diffweight[self.table[x]]
            self.table[x] = root
            return root

    def Unite(self,x,y,w): #xとyをDiff(x,y)=W で繋げる
        w = w - self.Weight(y) + self.Weight(x)
        x,y = self.Find(x), self.Find(y)
        sx,sy = self.Size(x), self.Size(y)
        if x == y: return
        if self.rank[x] > self.rank[y]:
            self.table[y] = x
            self.size[x] = sx + sy
            self.diffweight[y] = w
        else:
            self.table[x] = y
            self.size[y] = sx + sy
            self.diffweight[x] = -w
            if self.rank[x] == self.rank[y]:
                self.rank[y] += 1

    def Check(self,x,y):
        return self.Find(x) == self.Find(y)

    def Size(self,x):
        return self.size[self.Find(x)]

    def Weight(self,x): # 重さ(根からの距離)
        self.Find(x)
        return self.diffweight[x]

    def Diff(self,x,y): # 繋がってる二点間距離
        return self.Weight(y) - self.Weight(x)

# 優先度付きキュー
class HeapQueue:
    def __init__(self,flag): # flag == true 最小値pop / False 最大値pop
        if flag: self.inv = 1
        else: self.inv = -1
        self.hq = []
        heapq.heapify(self.hq)

    def push(self,x):
        heapq.heappush(self.hq,self.inv*x)

    def pop(self):
        return self.inv * heapq.heappop(self.hq)

# 動的中央値管理
class DynamicMedian:
    def __init__(self):
        self.Hq = HeapQueue(True) #Lqより多く
        self.Hv = None
        self.Lv = None
        self.Lq = HeapQueue(False)
        self.N = 0

    def pop(self,x):
        if self.N == 0:
            self.Hv = x
        elif self.N == 1:
            if x <= self.Hv:
                self.Lv = x
            else:
                self.Lv,self.Hv = self.Hv,x
        elif self.N%2 == 0: # Hq と Lq が同数
            if self.Hv <= x:
                self.Hq.push(x)
            elif self.Lv < x < self.Hv:
                self.Hq.push(self.Hv)
                self.Hv = x
            elif x <= self.Lv:
                self.Hq.push(self.Hv)
                self.Hv = self.Lv
                self.Lv = self.Lq.pop()
                self.Lq.push(x)
        else: # Hq が一つ多い
            if self.Hv <= x:
                self.Lq.push(self.Lv)
                self.Lv = self.Hv
                self.Hv = self.Hq.pop()
                self.Hq.push(x)
            elif self.Lv < x < self.Hv:
                self.Lq.push(self.Lv)
                self.Lv = x
            elif x <= self.Lv:
                self.Lv.push(x)
        self.N += 1

    def median(self):
        if self.N%2 == 0:
            return (self.Hv+self.Lv)/2
        else:
            return self.Hv

#

###########################
#          幾何
###########################
def sgn(a):
    if a < -eps: return -1
    if a >  eps: return  1
    return 0

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        pass

    def tolist(self):
        return [self.x,self.y]

    def __add__(self,p):
        return Point(self.x+p.x, self.y+p.y)
    def __iadd__(self,p):
        return self + p

    def __sub__(self,p):
        return Point(self.x - p.x, self.y - p.y)
    def __isub__(self,p):
        return self - p

    def __truediv__(self,n):
        return Point(self.x/n, self.y/n)
    def __itruediv__(self,n):
        return self / n

    def __mul__(self,n):
        return Point(self.x*n, self.y*n)
    def __imul__(self,n):
        return self * n

    def __lt__(self,other):
        tmp = sgn(self.x - other.x)
        if tmp != 0:
            return tmp < 0
        else:
            return sgn(self.y - other.y) < 0

    def __eq__(self,other):
        return sgn(self.x - other.x) == 0 and sgn(self.y - other.y) == 0

    def abs(self):
        return math.sqrt(self.x**2+self.y**2)

    def dot(self,p):
        return self.x * p.x + self.y*p.y

    def det(self,p):
        return self.x * p.y - self.y*p.x

    def arg(self,p):
        return math.atan2(y,x)

# 点の進行方向 a -> b -> c
def iSP(a,b,c):
    tmp = sgn((b-a).det(c-a))
    if tmp > 0:   return 1   # 左に曲がる場合
    elif tmp < 0: return -1  # 右に曲がる場合
    else: # まっすぐ
        if sgn((b-a).dot(c-a)) < 0: return -2 # c-a-b の順
        if sgn((a-b).dot(c-b)) < 0: return  2 # a-b-c の順
        return 0 # a-c-bの順




# ab,cd の直線交差
def isToleranceLine(a,b,c,d):
    if sgn((b-a).det(c-d)) != 0: return 1 # 交差する
    else:
        if sgn((b-a).det(c-a)) != 0: return 0 # 平行
        else: return -1 # 同一直線

# ab,cd の線分交差 重複，端点での交差もTrue
def isToleranceSegline(a,b,c,d):
    return sgn(iSP(a,b,c)*iSP(a,b,d))<=0 and sgn(iSP(c,d,a)*iSP(c,d,b)) <= 0

# 直線ab と 直線cd の交点 (存在する前提)
def Intersection(a,b,c,d):
    tmp1 = (b-a)*((c-a).det(d-c))
    tmp2 = (b-a).det(d-c)
    return a+(tmp1/tmp2)

# 直線ab と 点c の距離
def DistanceLineToPoint(a,b,c):
    return abs(((c-a).det(b-a))/((b-a).abs()))

# 線分ab と 点c の距離
def DistanceSeglineToPoint(a,b,c):
    if sgn((b-a).dot(c-a)) < 0: # <cab が鈍角
        return (c-a).abs()
    if sgn((a-b).dot(c-b)) < 0: # <cba が鈍角
        return (c-b).abs()
    return DistanceLineToPoint(a,b,c)

# 直線ab への 点c からの垂線の足
def Vfoot(a,b,c):
    d = c + Point((b-a).y,-(b-a).x)
    return Intersection(a,b,c,d)

# 多角形の面積
def PolygonArea(Plist):
    #Plist = ConvexHull(Plist)
    L = len(Plist)
    S = 0
    for i in range(L):
        tmpS = (Plist[i-1].det(Plist[i]))/2
        S += tmpS
    return S

# 多角形の重心
def PolygonG(Plist):
    Plist = ConvexHull(Plist)
    L = len(Plist)
    S = 0
    G = Point(0,0)
    for i in range(L):
        tmpS = (Plist[i-1].det(Plist[i]))/2
        S += tmpS
        G += (Plist[i-1]+Plist[i])/3*tmpS
    return G/S

# 多角形 包含点
def InclusionPoint(Plist,p):
    L = len(Plist)
    cnt = 0
    for i in range(L):
        a,b = Plist[i-1],Plist[i]
        if (a.y <= p.y < b.y) or (b.y <= p.y < a.y):
            vt = (p.y-a.y) /(b.y-a.y)
            if p.x < a.x + vt*(b.x-a.x):
                cnt += 1
    return cnt%2 == 1


# 凸法
def ConvexHull(Plist):
    Plist.sort()
    L = len(Plist)
    qu = deque([])
    quL = 0
    for p in Plist:
        while quL >= 2 and iSP(qu[quL-2],qu[quL-1],p) == 1:
            qu.pop()
            quL -= 1
        qu.append(p)
        quL += 1

    qd = deque([])
    qdL = 0
    for p in Plist:
        while qdL >= 2 and iSP(qd[qdL-2],qd[qdL-1],p) == -1:
            qd.pop()
            qdL -= 1
        qd.append(p)
        qdL += 1

    qd.pop()
    qu.popleft()
    hidari = list(qd) + list(reversed(qu)) # 左端開始，左回りPlist
    return hidari


#####################
#        数学       #
#####################

class Combination:
    def __init__(self,N):
        self.fac = [1]*(N+1)
        for i in range(1,N+1):
            self.fac[i] = (self.fac[i-1]*i)%mod
        self.invmod = [1]*(N+1)
        self.invmod[N] = pow(self.fac[N],mod-2,mod)
        for i in range(N,0,-1):
            self.invmod[i-1] = (self.invmod[i]*i)%mod

    def calc(self,n,k):#nCk
        return self.fac[n]*self.invmod[k]%mod *self.invmod[n-k] %mod

# 篩
prime = []
limit = math.sqrt(koho[-1])
while True:
    p = koho[0]
    if limit <= p:
        prime = prime + koho
        break
    else:
        prime.append(p)
        koho = [e for e in koho if e%p != 0]

# gcd
def gcd(a,b):
	while b:
		a,b = b, a%b
	return a

def lcm(a,b):
	return a*b // gcd(a,b)

# 行列累乗
def Matdot(A,B):
    C = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k]*B[k][j]
            C[i][j] %= mod
    return C

def power(aa,k):
    if k == 1:
        return aa
    elif k%2 == 0:
        tmp = power(aa,k//2)
        return Matdot(tmp,tmp)
    else:
        tmp = power(aa,(k-1)//2)
        return Matdot(Matdot(tmp,tmp),aa)

#
def is_prime(x):
    if x < 2: return False # 2未満に素数はない
    if x == 2 or x == 3 or x == 5: return True # 2,3,5は素数
    if x % 2 == 0 or x % 3 == 0 or x % 5 == 0: return False # 2,3,5の倍数は合成数

    # 疑似素数で割る
    prime = 7
    step = 4
    while prime <= math.sqrt(x):
        if x % prime == 0: return False
        prime += step
        step = 6 - step

    return True

# 二分累乗
def ex_square(n,k): # pow(n,k,mod)
	if k == 0:
		ans = 1
	elif k % 2 == 0:
		ans = ex_square(n, k//2) ** 2
	else:
		ans = ex_square(n,k-1) * n
	ans %= mod
	return ans

#ビットマスク(特定の桁だけ)
a = 10100
> (a>>0) & 1 = 0
> (a>>1) & 1 = 0
> (a>>2) & 1 = 1
> (a>>3) & 1 = 0
> (a>>4) & 1 = 1

# next_combination (n桁でk箇所bitが立ってる物を全探索)
def next_com(bit):
	x = bit & -bit
	y = bit + x
	return (((bit & ~y) // x) >> 1) | y
n,k = 5,3
bit = (1<<k)-1
ans = 0
while bit < (1<<n):
	for i in range(n):
		if (bit>>i) & 1:
            # 処理
	bit = next_com(bit)


#bitが立ってる数をカウント
def bitcount(bits):
    bits = (bits & 0x55555555) + (bits >> 1 & 0x55555555)
    bits = (bits & 0x33333333) + (bits >> 2 & 0x33333333)
    bits = (bits & 0x0f0f0f0f) + (bits >> 4 & 0x0f0f0f0f)
    bits = (bits & 0x00ff00ff) + (bits >> 8 & 0x00ff00ff)
    return (bits & 0x0000ffff) + (bits >>16 & 0x0000ffff)

#
##### itertools #####
seq = ('a', 'b', 'c', 'd', 'e')

# 並べ方
list(itertools.permutations(seq))
>[('a', 'b', 'c', 'd', 'e'),
  ('a', 'b', 'c', 'e', 'd'),
  ('a', 'b', 'd', 'c', 'e'),
  ('a', 'b', 'd', 'e', 'c'),
           中略
  ('e', 'd', 'c', 'a', 'b'),
  ('e', 'd', 'c', 'b', 'a')]

# 何個かを選ぶ並べ方
list(itertools.permutations(seq, 3))
> [('a', 'b', 'c'),
  ('a', 'b', 'd'),
  ('a', 'b', 'e'),
  ('a', 'c', 'b'),
       中略
  ('e', 'd', 'a'),
  ('e', 'd', 'b'),
  ('e', 'd', 'c')]

# 重複を許す順列 ([True,False]でやればbit全探索ができる)
list(itertools.product(A, repeat=3))
>[('a', 'a', 'a'),
  ('a', 'a', 'b'),
  ('a', 'a', 'c'),
  ('a', 'b', 'a'),
  ('a', 'b', 'b'), …

# 組み合わせ
list(itertools.combinations(seq,5))
> [('a', 'b', 'c', 'd', 'e')]

# 何個かを選ぶ組み合わせ
list(itertools.combinations(seq,3))
[('a', 'b', 'c'),
 ('a', 'b', 'd'),
 ('a', 'b', 'e'),
 ('a', 'c', 'd'),
 ('a', 'c', 'e'), …

# 重複を許す組み合わせ
list(itertools.combinations_with_replacement(A, 3))
[('a', 'a', 'a'),
 ('a', 'a', 'b'),
 ('a', 'a', 'c'),
 ('a', 'b', 'b'),
 ('a', 'b', 'c'), …
