import heapq
def inp(): return int(input())
def inpl(): return list(map(int, input().split()))
def inpl_str(): return list(input().split())


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
