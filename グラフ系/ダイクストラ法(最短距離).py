def dijkstra(N,S,T):
    weight = [INF]*N
    weight[S] = 0
    q = [[0,S]]
    heapq.heapify(q)
    while q:
        w0,s = heapq.heappop(q)
        for t,w in lines[s]:
            w += w0
            if weight[t] > w:
                heapq.heappush(q,[w,t])
                weight[t] = w

    return weight[T]
