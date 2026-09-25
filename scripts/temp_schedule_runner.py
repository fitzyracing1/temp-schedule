#!/usr/bin/env python3
"""Temp schedule runner — high / low / low."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

SCHEDULE = ["high", "low", "low"]
TEMP = {"high": 1.0, "low": 0.4}
ROLE = {
    1: ("high", "invent"),
    2: ("low", "build"),
    3: ("low", "freeze + enforce metric"),
}
LANES = ("BUILD", "SHIP", "FIND", "DESIGN", "TRACK", "SCHEDULE", "COMPUTE")
METRIC = "2 * x * c - d = 1"


def plan(job: str, lane: str) -> dict:
    lane = lane.upper()
    if lane not in LANES:
        raise SystemExit(f"lane must be one of {LANES}")
    passes = []
    for i in range(1, 4):
        name, role = ROLE[i]
        passes.append(
            {
                "pass": i,
                "name": name,
                "temp": TEMP[name],
                "role": role,
                "done": False,
            }
        )
    return {
        "job": job,
        "lane": lane,
        "temp_schedule": SCHEDULE,
        "metric": METRIC,
        "created": datetime.now(timezone.utc).isoformat(),
        "passes": passes,
        "rule": "do not skip; do not return to high after pass 1; two lows at the same T; third low freezes + metric",
    }


def render(p: dict) -> str:
    lines = [
        f"job:   {p['job']}",
        f"lane:  {p['lane']}",
        f"sched: {p['temp_schedule']}",
        f"metric:{p['metric']}",
        "",
    ]
    for step in p["passes"]:
        lines.append(
            f"  {step['pass']}. {step['name']:6}  T={step['temp']:<4}  {step['role']}"
        )
    lines += ["", p["rule"]]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="high-low-low temperature runner")
    ap.add_argument("--job", required=True, help="goal text")
    ap.add_argument("--lane", default="BUILD", help="BUILD SHIP FIND DESIGN TRACK SCHEDULE COMPUTE")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    p = plan(args.job, args.lane)
    if args.json:
        print(json.dumps(p, indent=2))
    else:
        print(render(p))


if __name__ == "__main__":
    main()
