# Overnight run

Observed journal window: 2026-11-02 19:26:37 Pacific Standard Time through 2026-11-03 08:01:07 Pacific Standard Time.
Duration: 12h 34m 30s. Minimum eight-hour window: met.
Times below use the computer's local time zone (America/Los_Angeles for this run).
Source: logs/main.jsonl. No message bodies or recipient addresses are included.

| Wake-up time | Source | Model calls / turns | Input tokens | Output tokens | Total tokens | Dollars |
|---|---|---:|---:|---:|---:|---|
| 2026-11-02 19:32:34 Pacific Standard Time | telegram | 1 | 3997 | 6 | 4003 | Not priced |
| 2026-11-03 08:00:49 Pacific Standard Time | schedule morning-papers | 4 | 18574 | 365 | 18939 | Not priced |

Totals: 2 wake-ups, 5 model calls, 22571 input + 371 output = 22942 tokens.
Cached input reported: 17152 tokens (already part of input; not added twice).
Model calls with no active/relevant wake: **0**.
Dollar amounts are unavailable because this harness enforces a token budget without configured model prices.

## Failures observed

- 2026-11-03 00:22:20 Pacific Standard Time: watcher_error, watcher=email, type=RuntimeError.

The log proves the event/usage timing above; it is not an independent power/sleep monitor. Check the morning output and service state separately.
