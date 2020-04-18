def Matdot(A,B):
    C = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k]*B[k][j]
            C[i][j] %= mod
    return C

def power(aa,k):
    if k == 1:
        return aa
    elif k%2 == 0:
        tmp = power(aa,k//2)
        return Matdot(tmp,tmp)
    else:
        tmp = power(aa,(k-1)//2)
        return Matdot(Matdot(tmp,tmp),aa)
