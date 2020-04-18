

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
