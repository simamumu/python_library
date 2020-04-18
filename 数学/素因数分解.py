
# 先にふるってprimesを作る
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


N = 10000
MAX = 100000
primes = hurui(math.sqrt(MAX))

# N を素因数分解
def factorization(N):
    ans = defaultdict(int)
    L = len(primes)
    pind = 0
    while N > 1:
        p = primes[pind]
        while N%p == 0:
            N //= p
            ans[p] += 1
        pind += 1
        if pind >= L:
            ans[N] += 1
            break
    return ans

facs = factorization(N)

for p,n in facs.items():
    print(p,n)
