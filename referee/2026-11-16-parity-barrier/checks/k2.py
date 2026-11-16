import numpy as np, scipy.linalg as sl
def run(n,eps):
    h=1/n; a=round((1-eps)*n); B=round((1+eps)*n)
    cells=[(i,j) for i in range(2*n) for j in range(2*n) if i+j+2<=2*n]
    idx={c:t for t,c in enumerate(cells)}; N=len(cells)
    # constraints: column y-cell j>=B: sum_i F_ij=0 ; row x-cell i>=B: sum_j F_ij =0
    C=[]
    for j in range(B,2*n):
        r=np.zeros(N); 
        for (i,jj),t in idx.items():
            if jj==j: r[t]=1
        if r.any(): C.append(r)
    for i in range(B,2*n):
        r=np.zeros(N)
        for (ii,j),t in idx.items():
            if ii==i: r[t]=1
        if r.any(): C.append(r)
    C=np.array(C)
    Z=sl.null_space(C) if len(C) else np.eye(N)
    # J = sum_{i<a} h*(h*sum_j F_ij)^2 + same for columns
    P=[]
    for i in range(a):
        r=np.zeros(N)
        for (ii,j),t in idx.items():
            if ii==i: r[t]=h
        P.append(r*np.sqrt(h))
    for j in range(a):
        r=np.zeros(N)
        for (i,jj),t in idx.items():
            if jj==j: r[t]=h
        P.append(r*np.sqrt(h))
    P=np.array(P)
    Jm=Z.T@P.T@P@Z; Im=h*h*np.eye(Z.shape[1])
    w=sl.eigh(Jm,Im,eigvals_only=True)
    return w[-1]
for n,eps in [(8,0.25),(12,0.25),(16,0.125),(10,0.1),(20,0.5),(16,0.75)]:
    print(n,eps,run(n,eps))
