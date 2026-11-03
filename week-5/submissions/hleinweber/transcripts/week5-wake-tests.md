# Week 5 step 1: live wake-up checks

Evidence: student report in the homework session, November 2, 2026.

- Telegram test response: "Telegram wake-up received."
- Email test produced a Telegram response: "Acknowledged the email wake-up test. No reply needed. How can I assist you further?"
- No terminal activity was observed during the idle interval.
- Two model calls total across the two tests.
- Student explanation: an empty event queue causes no model call; the harness wakes the model only when an event requires one.

This is a manual functional check, not the required eight-hour overnight demo.
