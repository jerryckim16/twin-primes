#!/usr/bin/env python3
"""One regression driver for the project's committed exact certificates (weekly review of 23 Nov 2026).

It replaces the per-run from-scratch regressions of Sessions 42-47. Run it at most once a month (or after a change to
a certification program). Each job re-runs ONE program on its committed input, in a scratch directory, and compares the
output with the committed JSON field by field (timing fields ignored). This checks reproducibility of program 1 only;
it is NOT a second independent program and adds nothing to the "two programs" standard.

usage:
  python3 code/cap6/regress_all.py --list                 # show the jobs and their cost
  python3 code/cap6/regress_all.py --run JOB [JOB ...]    # run the named jobs (sequentially), write a report
  python3 code/cap6/regress_all.py --run all              # everything (about 10 core-hours; run alone, ~2 GB/worker)
Report: code/cap6/regress_all_<UTC date>.json.  Requirements: python-flint (capped_check, oai186_loss_inner), gmpy2
(oai186_IH, oai186_J); use /usr/bin/python3 if python-flint is installed there.
Not yet included: the 186 main terms (code/oai186_IH.py, code/oai186_J.py write fixed output paths; re-run them by hand
as in Session 44 and compare with code/oai186_IH.json, code/oai186_J.json) and the outer loss parts.
"""
import json, os, subprocess, sys, tempfile, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable
TIMING = {"seconds", "peak_rss_MB", "elapsed", "time", "wall", "procs"}

INNER = ["I2new_L1_L2_L3", "I2new_L4_L5_L6", "I2new_P1_P2", "I2new_P3_P4_H", "I2old_L1_L4_L5", "I2old_L2_L3",
         "I2old_P1_H", "I52new_L10_L11_P1", "I52new_L1_L2_L3", "I52new_L4_L5_L6", "I52new_L7_L8_L9", "I52new_P2_P3",
         "I52new_P4_P5_H", "I52old_L1_L2_L3", "I52old_L4_L5_L6", "I52old_L7_P1", "I52old_P2_H"]


def inner_job(name):
    g, *comps = name.split("_")
    group = {"I2new": "I2new", "I2old": "I2old", "I52new": "I5/2new", "I52old": "I5/2old"}[g]
    return {"cost": "one core, 10-25 min, ~1.5 GB",
            "cmd": lambda out: [PY, "code/oai186_loss_inner.py", "--group", group, "--comp", ",".join(comps),
                                "--part", out],
            "ref": f"code/cap6/loss_inner/part_{name}.json"}


JOBS = {
    "240": {"cost": "4 procs, ~5 min",
            "cmd": lambda out: [PY, "code/capped_check.py", "code/cap6/P_capfree_D20_u.json", "--out", out,
                                "--procs", "3", "--quiet"],
            "ref": "code/cap6/check_capfree_D20.json"},
    "236": {"cost": "3 procs, ~1 h, ~2 GB/worker",
            "cmd": lambda out: [PY, "code/capped_check.py", "code/cap6/P_sy236_u.json", "--out", out,
                                "--procs", "3", "--quiet"],
            "ref": "code/cap6/check_sy236.json"},
}
for n in INNER:
    JOBS["186-inner-" + n] = inner_job(n)


def strip(d):
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items() if k not in TIMING}
    if isinstance(d, list):
        return [strip(v) for v in d]
    return d


def run(name):
    job = JOBS[name]
    tmp = tempfile.mkdtemp(prefix="regress_")
    out = os.path.join(tmp, "out.json")
    t0 = time.time()
    p = subprocess.run(job["cmd"](out), cwd=ROOT, capture_output=True, text=True)
    res = {"job": name, "returncode": p.returncode, "seconds": round(time.time() - t0, 1), "ref": job["ref"]}
    if p.returncode != 0 or not os.path.exists(out):
        res["status"] = "FAILED"
        res["stderr_tail"] = p.stderr[-2000:]
        return res
    new = strip(json.load(open(out)))
    old = strip(json.load(open(os.path.join(ROOT, job["ref"]))))
    res["status"] = "identical" if new == old else "DIFFERS"
    if new != old and isinstance(new, dict) and isinstance(old, dict):
        res["differing_fields"] = sorted(k for k in set(new) | set(old) if new.get(k) != old.get(k))
    return res


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--list":
        for k, v in JOBS.items():
            print(f"{k:28s} {v['cost']:32s} ref {v['ref']}")
        sys.exit(0)
    assert a[0] == "--run"
    names = list(JOBS) if a[1:] == ["all"] else a[1:]
    report = {"date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "python": PY, "jobs": []}
    for n in names:
        r = run(n)
        print(json.dumps(r), flush=True)
        report["jobs"].append(r)
    report["all_identical"] = all(r["status"] == "identical" for r in report["jobs"])
    fn = os.path.join(ROOT, "code", "cap6", f"regress_all_{report['date'][:10]}.json")
    json.dump(report, open(fn, "w"), indent=1)
    print("all identical:", report["all_identical"], "->", os.path.relpath(fn, ROOT))
