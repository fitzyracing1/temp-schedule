# temp-schedule

Three-pass temperature runner for every AI job.

```
Temp_schedule = ["high", "low", "low"]
# high   → invent
# low    → build
# low    → freeze + enforce metric
```

T means temperature. Both later passes are named low. The third low changes job, not T.

## Run

```bash
python scripts/temp_schedule_runner.py --job "goal text" --lane BUILD
```

Lanes: BUILD SHIP FIND DESIGN TRACK SCHEDULE COMPUTE

Temps: high = 1.0 invent, low = 0.4 build, low = 0.4 freeze + enforce `2 * x * c - d = 1`.
