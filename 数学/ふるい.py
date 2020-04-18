
def hurui(N):
    koho = list(range(2,N))
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

    return prime
