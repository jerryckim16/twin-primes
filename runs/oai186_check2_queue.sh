#!/bin/sh
# runs the remaining J caps of oai186_check2.py, at most 3 heavy python processes at a time (OOM at 4)
cd /home/user/twin-primes
for b in 44781 35419 35265; do
  [ -f code/cap6/oai186_check2_J_b$b.json ] && continue
  while [ $(pgrep -fc "^python3 code/oai186_check2.py") -ge 3 ]; do sleep 20; done
  nohup python3 code/oai186_check2.py --jcap $b > runs/oai186_check2_J_$b.log 2>&1 &
  sleep 60
done
wait
