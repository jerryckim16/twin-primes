#!/bin/sh
# one outer component at 128 bits; skips it if its part file exists (resume)
cd "$(dirname "$0")/.."
g="$1"; c="$2"; tag=$(echo "$g" | tr -d '/')_$c
out=code/cap6/loss_outer/part_$tag.json
[ -f "$out" ] && exit 0
python3 code/oai186_loss_outer.py --group "$g" --comp "$c" --prec 128 --part "$out" > runs/loss_outer_$tag.log 2>&1
