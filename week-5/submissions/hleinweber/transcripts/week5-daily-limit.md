# Week 5 daily-token limit demo

Date: November 2, 2026.

After the kill-switch demo, the student reported /status showing four model calls and 6,604 tokens today. The daily budget in limits.toml was temporarily lowered from 250,000 to 1 token, below the usage already recorded. The running harness reloads the file; no restart was required.

The student sent the budget test message and confirmed that the subsequent status still reported four model calls. This verifies that the held request caused no additional model call. The exact budget-warning text was not supplied in the student's confirmation.

The budget was restored to 250,000 tokens after confirmation. The held request may run once the harness sees the restored budget, so its later response or a subsequent fifth model call is expected. Daily usage was not reset.
