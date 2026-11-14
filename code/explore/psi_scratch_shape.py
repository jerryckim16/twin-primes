import sys; sys.path.insert(0,'/home/user/twin-primes/code/explore')
import numpy as np
from psi_scratch_wform import I_w, k, tau, E2
a=1.037
for others in [[E2]*9, [E2]*10, [E2]*5, [0.02]*10, [0.3,0.3], [E2]*9+[0.03]*5, [0.0]]:
    o=np.array(others+[0]*(k-2-len(others)))
    ymax=min(E2,tau-o.sum()); ys=np.linspace(0,ymax,41)
    v=np.array([I_w(a,np.append(o,y)) for y in ys])
    d=np.diff(v)/np.diff(ys)
    print(others[:3],len(others),"I(0)=%.6f I(end)=%.6f"%(v[0],v[-1]))
    print("  dI/dy:",np.round(d[::4],4))
