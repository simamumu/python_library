

N,M,P = map(int,input().split())

def ex_square(n,k): # pow(n,k,mod)
	if k == 0:
		ans = 1
	elif k % 2 == 0:
		ans = ex_square(n, k//2) ** 2
	else:
		ans = ex_square(n,k-1) * n
	ans %= mod
	return ans

print(ex_square(N,P))
