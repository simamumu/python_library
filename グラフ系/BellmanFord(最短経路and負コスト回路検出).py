
#ベルマンフォード(始点と終点が決まってる時)
def BellmanFord(Start,Goal):
    Costs=[INF]*N
    Costs[Start] = 0
    upd8s = [True]*N
    for i in range(2*N): #2N回ループ(負閉路の検出までみる)
        will_upd8s = [False]*N
        for s in range(N):
            if not upd8s[s]: continue    #前回更新してないので見ない
            for t,c in lines[s]:
                if c + Costs[s] < Costs[t]:
                    Costs[t] = Costs[s]+c
                    will_upd8s[t] = True #更新した点だけ次に見る
                    if i >= N:
                        Costs[t] = -INF

        if i == N-1: #Nループ目のGoalのCostを記録
            tmp = Costs[Goal]

        upd8s = will_upd8s[:]

    if tmp != Costs[Goal]:
        return -INF
    else:
        return Costs[Goal]
