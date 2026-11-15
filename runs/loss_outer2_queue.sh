#!/bin/bash
# two workers over the remaining components (largest table E first)
cd /home/user/twin-primes
worker() { for c in "$@"; do python3 code/oai186_loss_outer2.py --comp $c --out code/cap6/loss_outer2/part_$c.json > runs/loss_outer2_$c.log 2>&1; done; }
worker P2 P4 P5 P6 P10 P11 P12 L20 L19 &
worker P3 P1 P9 P7 P8 H L22 L21 &
wait
