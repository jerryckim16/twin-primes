import itertools, numpy as np, random
from scipy.optimize import linprog
def feasible(k,E):
    free=[S for r in range(k+1) for S in itertools.combinations(range(k),r) if not any(set(e)<=set(S) for e in E)]
    A=np.zeros((k+1,len(free)))
    for t,S in enumerate(free):
        for i in S: A[i,t]=1
        A[k,t]=1
    b=np.array([0.5]*k+[1])
    r=linprog(np.zeros(len(free)),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
    return r.status==0
random.seed(1); bad=0
for trial in range(400):
    k=random.randint(2,8); H=sorted(random.sample(range(0,30),k)); m=random.randint(1,3); g=random.randint(0,20)
    E=[e for e in itertools.combinations(range(k),m+1) if H[e[-1]]-H[e[0]]<=g]
    crit=all(sum(1 for h in H if a<=h<=a+g)<=2*m for a in H)
    if feasible(k,E)!=crit: bad+=1; print('MISMATCH',H,m,g)
print('bad',bad)
