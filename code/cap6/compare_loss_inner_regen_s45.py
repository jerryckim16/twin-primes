#!/usr/bin/env python3
"""Session 45 regression: compare the from-scratch re-runs of three groups of 186 inner loss components
(code/cap6/loss_inner_regen_s45/part_*.json, produced by code/oai186_loss_inner.py with the commands below) with the
committed parts in code/cap6/loss_inner/. Writes code/cap6/compare_loss_inner_regen_s45.json.

Re-run commands (one core each, ~25 min, ~1.5 GB):
  python3 code/oai186_loss_inner.py --group I2old   --comp L2,L3    --part code/cap6/loss_inner_regen_s45/part_I2old_L2_L3.json
  python3 code/oai186_loss_inner.py --group I5/2old --comp L1,L2,L3 --part code/cap6/loss_inner_regen_s45/part_I52old_L1_L2_L3.json
  python3 code/oai186_loss_inner.py --group I5/2new --comp L7,L8,L9 --part code/cap6/loss_inner_regen_s45/part_I52new_L7_L8_L9.json
"""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
out = {"note": "fields other than timing (seconds, peak_rss_MB) must agree exactly", "parts": {}}
allsame = True
for f in sorted(glob.glob(os.path.join(HERE, "loss_inner_regen_s45", "part_*.json"))):
    name = os.path.basename(f)
    new = json.load(open(f))
    old = json.load(open(os.path.join(HERE, "loss_inner", name)))
    strip = lambda d: {k: v for k, v in d.items() if k not in ("seconds", "peak_rss_MB")}
    same = strip(new) == strip(old)
    allsame &= same
    diffs = [k for k in set(strip(new)) | set(strip(old)) if strip(new).get(k) != strip(old).get(k)]
    out["parts"][name] = {"identical": same, "differing_fields": diffs,
                          "seconds_old": old.get("seconds"), "seconds_new": new.get("seconds")}
    print(name, "identical" if same else f"DIFFERS in {diffs}")
out["all_identical"] = allsame
json.dump(out, open(os.path.join(HERE, "compare_loss_inner_regen_s45.json"), "w"), indent=1)
print("all identical:", allsame)
