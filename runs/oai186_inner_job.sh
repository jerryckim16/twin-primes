#!/bin/sh
# one queue item: group comps ; skips items whose part file exists (resume)
cd "$(dirname "$0")/.."
g="$1"; c="$2"; tag=$(echo "$g" | tr -d '/')_$(echo "$c" | tr ',' '_')
out=code/cap6/loss_inner/part_$tag.json
[ -f "$out" ] && exit 0
python3 code/oai186_loss_inner.py --group "$g" --comp "$c" --part "$out" > runs/loss_inner_$tag.log 2>&1
