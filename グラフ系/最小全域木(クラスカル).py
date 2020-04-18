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

    def Unite(self,x,y): 
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


N,M = inpl()
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

print(weight)
