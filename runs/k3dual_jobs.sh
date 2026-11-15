cd /home/user/twin-primes
for e in 0.125 0.25 0.375; do for m in full disj none; do /usr/bin/python3 code/parity/k3_thm314_dual.py $e $m 16 24 32 40; done; done
for e in 0.05 0.15 0.35 0.45; do for m in full disj; do /usr/bin/python3 code/parity/k3_thm314_dual.py $e $m 20 40; done; done
