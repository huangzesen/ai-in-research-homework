# Week 5: real compaction and recall

The conversation fixture was explicitly synthetic. A real initial model call
reported 1,517 input tokens. Disposable context then raised the reported input
to 26,262, crossing the owner-selected 20,000-token trigger. The owner approved
saving the demo facts to memory/MEMORY.md. The pre-compaction checkpoint used
ordinary tool dispatch and owner approval; its extra memory read was redundant.

One summary call reported 26,613 input / 1,311 output tokens. The new conversation
kept the refreshed system prompt, summary and six recent messages intact, with
complete tool-call/result pairs. The initial post-compaction estimate was 2,789.
The owner's actual recall question then reported 2,331 input tokens. The reply:

> Project codename: SUNTHREAD-482. Target interval: interval-b.

The owner confirmed receiving this correct reply. It checks continuity after
compaction, not exclusive attribution to a single memory representation: the
identifiers were in persistent memory, the summary and the retained save turn.
The whole demo used seven real model requests and 139,088 reported tokens.

Review note: the preserved generated summary incorrectly described the important
identifiers as nonessential in one sentence, despite retaining their values.
The original fixture designated them important. Future prompts were tightened;
the original output remains unchanged. The reported after-count, not the earlier
estimate, is the compaction measurement.

The private original summary is logs/compactions/20261103T044919189622Z.md;
the synthetic original context is logs/compactions/demo-fixture.txt. No live
inbox content or credentials were part of this fixture.

Student observation of one omitted detail: "Omitted individual padding rows."

The student supplied this observation after reviewing the summary. Step 4
and its learning checkpoint are complete.

## Actual generated summary

Owner name is redacted; the original priority-labeling mistake is preserved.

```markdown
# Goal
Conversation compaction test with synthetic data. Preserve key identifiers and demo metadata for future continuation after memory write.

# Done
- Synthetic facts demo loaded (2026-11-02 20:48:46 PST)
- Synthetic padding context loaded (2026-11-02 20:48:48 PST)
- Memory/MEMORY.md read and updated with key identifiers
- Key identifiers preserved for recall check

# Open
- Continue conversation after compaction
- No unresolved tasks; compaction workflow in progress

# Decisions
- Save memory with exact identifiers (SUNTHREAD-482, interval-b, amber)
- Use memory tool to write (not declined)
- Preserve only nonessential demo codename and interval

# Exact
- **SUNTHREAD-482**: project codename
- **interval-b**: target interval
- **amber**: demo note color
- **memory/MEMORY.md**: updated file path
- Timestamps: 2026-11-02 20:48:46 PST, 2026-11-02 20:48:48 PST

# People
- [owner] (owner)
- Jasmine's Agent (this assistant)
- harness (system managing compaction, polling, and approvals)
```
