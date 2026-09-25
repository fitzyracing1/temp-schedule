---
name: temp-schedule
description: Run every AI job on the high-low-low temperature schedule. Activate for temp schedule, high low low, temperature runner, invent-build-freeze, or when the user wants all AI work staged as invent then build then freeze-plus-metric at the same low T.
metadata:
  type: workflow
  version: "1.2"
  schedule: high-low-low
---

# Temp Schedule

Fixed three-pass temperature runner for every AI job.

```
Temp_schedule = ["high", "low", "low"]
# high   → invent
# low    → build
# low    → freeze + enforce metric
```

T means temperature. Both later passes are named low. The third low changes job, not T.

## Temperatures

- high — 1.0  invent
- low  — 0.4  build
- low  — 0.4  freeze + enforce metric

Do not skip a stage. Do not stay on high after pass 1. Pass 2 and pass 3 share T=0.4.

## When activated

1. Name the job and the lane (BUILD / SHIP / FIND / DESIGN / TRACK / SCHEDULE / COMPUTE).
2. Pass high — invent only.
3. Pass low — build the artifact.
4. Pass low — freeze and enforce `2 * x * c - d = 1`. Do not reopen invention.
5. Log the three passes. One job, three passes, then stop.

## Runner

```bash
python scripts/temp_schedule_runner.py --job "goal text"
python scripts/temp_schedule_runner.py --job "goal text" --lane BUILD
```

## Invariants

- T means temperature.
- Names are high, low, low.
- Third low freezes and enforces the metric at the same T as build.
- One job, three passes, then stop.
