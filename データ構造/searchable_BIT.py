class Searchable_BIT():
    def __init__(self,N):
        self.N = N
        self.node = [0]*(self.N+1)
        self.cnt = 0

    def add(self,a): # 要素 x を追加
        x = a
        self.cnt += 1
        while x <= self.N:
            self.node[x] += 1
            x += x & -x

    def delete(self,x): # 要素 x を削除
        self.cnt -= 1
        while x <= self.N:
            self.node[x] -= 1
            x += x & -x

    def count(self,x): # x以下の要素数
        tmp = 0
        while x > 0:
            tmp += self.node[x]
            x -= x & -x
        return tmp

    def get_maxval(self):
        return self.get_lower_i(self.cnt)

    def get_lower_i(self,i): # i 番目に小さい要素を取得
        NG = -1
        OK = self.N
        while OK-NG > 1:
            mid = (OK+NG)//2
            #print(OK,NG,self.count(mid))
            if self.count(mid) >= i:
                OK = mid
            else:
                NG = mid
        return OK
