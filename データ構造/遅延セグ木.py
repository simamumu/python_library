class LazySegmentTree:
    def __init__(self,N,d):
        self.b0 = (N-1).bit_length()
        self.N0 = 2**self.b0
        self.node = [d]*(self.N0*2)
        #self.lazy = [0]*(self.N0*2) # RSQ
        self.lazy = [None]*(self.N0*2) # RMQ

    def gindex(self,l,r):
        L = l + self.N0
        R = r + self.N0
        lm = (L // (L & -L)) >> 1
        rm = (R // (R & -R)) >> 1
        while L < R:
            if R <= rm:
                yield R
            if L <= lm:
                yield L
            L >>= 1; R >>= 1
        while L:
            yield L
            L >>= 1

    def eval(self,*ids):
        for i in reversed(ids):
            v = self.lazy[i-1]
            #if v == 0: # RSQ
            if v is None: # RMQ
                continue
            # 子の lazy に伝播
            self.lazy[2*i-1] = self.propagates(self.lazy[2*i-1],v)
            self.lazy[2*i]   = self.propagates(self.lazy[2*i],v)
            # 子の node に伝播
            self.node[2*i-1] = self.propagates(self.node[2*i-1],v)
            self.node[2*i]   = self.propagates(self.node[2*i],v)

            #self.lazy[i-1] = 0 # RSQ
            self.lazy[i-1] = None # RMQ

    def update_query(self,l,r,x): # [l,r)の値をxに更新
        # bottom-up に index を列挙
        *indexs, = self.gindex(l, r)

        # top-down にlazyの値を伝搬
        self.eval(*indexs)

        # 区間[l, r)のnode, lazyの値を更新
        L = self.N0 + l
        R = self.N0 + r
        while L < R:
            if R & 1:
                R -= 1
                self.lazy[R-1] = self.update_val(self.lazy[R-1],R-1,x)
                self.node[R-1] = self.update_val(self.node[R-1],R-1,x)
            if L & 1:
                tmp = 2 ** (self.b0 - (L.bit_length()-1))
                self.lazy[L-1] = self.update_val(self.lazy[L-1],L-1,x)
                self.node[L-1] = self.update_val(self.node[L-1],L-1,x)
                L += 1
            L >>= 1; R >>= 1

        # 伝搬させた区間について、bottom-up にnodeの値を伝搬する
        for i in indexs:
            self.node[i-1] = self.process(self.node[2*i-1], self.node[2*i])

    def get_query(self,l,r):
        # トップダウンにlazyの値を伝搬
        self.eval(*self.gindex(l, r))
        L = self.N0 + l
        R = self.N0 + r

        # 区間[l, r)の最小値を求める
        #s = 0 # RSQ
        s = INF
        while L < R:
            if R & 1:
                R -= 1
                s = self.process(s, self.node[R-1])
            if L & 1:
                s = self.process(s, self.node[L-1])
                L += 1
            L >>= 1; R >>= 1
        return s

    def update_val(self,v,ind,x): # ind の値v を x で update
        L = 2 ** (self.b0 - ((ind+1).bit_length()-1)) # 区間長
        #return v + x*L # RSQ
        return x # RMQ

    def propagates(self,x,v): # 親(val=v) -> 子(val=x) に伝播させる値
        #return x + v//2 # RSQ
        return v # RMQ

    def process(self,x,y): #x,yが子の時，親に返る値
        #return x+y # RSQ
        return min(x,y) #RMQ
