# Week 5: live daily token limit

After the phone kill-switch test, the helper temporarily set tokens_per_day
to 1. The owner sent a fresh budget-test question. The harness refused a new
model request and Telegram accepted its tokens_per_day limit notice. The owner
confirmed receiving that notice. The recorded additional model-request count
was zero.

The preceding real requests had already used more than this temporary cap;
the test did not ask the model to obey a budget instruction. The check and
notification ran in code. The exact original limits file was restored to
250,000 tokens/day, the demo's temporary block was cleared, and the preview
stopped. Today's recorded usage was retained rather than reset.

The current private receipt is validation/week-5-controls-live.json. The first
attempt's timeout is retained separately and is not counted as a pass. No
mailbox address, chat ID, key or private message body is included here.
