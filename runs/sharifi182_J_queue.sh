#!/bin/sh
# 182 J workers, at most 2 at a time (OOM at 3: ~6 GB each)
cd /home/user/twin-primes
for b in 140306 141720 141724 177528 177542 179967 186253 196608 246256; do
  [ -f code/data182/J_cap_$b.json ] && continue
  while [ $(pgrep -fc "^python3 code/sharifi182_J.py") -ge 2 ]; do sleep 20; done
  nohup python3 code/sharifi182_J.py --cap $b > runs/sharifi182_J_$b.log 2>&1 &
  sleep 90
done
wait
