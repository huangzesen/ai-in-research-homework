# Isolated forced-crash tests

These tests use real process termination, a fixed local tool side effect and a simulated mail provider. No model API, Telegram or real email was used. They do not replace the live service/email demo.

```json
{
  "tool_process_exit": 1,
  "tool_effects": 1,
  "interrupted_results": 1,
  "journal_prefix_preserved": true,
  "email_process_exit": 1,
  "simulated_deliveries": 1,
  "email_recovered_without_resend": true
}
```
