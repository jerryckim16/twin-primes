cd /home/user/twin-primes
for a in "1/6 12 24" "1/5 10 20" "2/9 18" "7/24 24" "3/10 10 20" "1/3 12 24"; do
  set -- $a; e=$1; shift
  /usr/bin/python3 -I code/parity/k3_arrangement_exact.py --eps $e --cert-each "$@"
done
