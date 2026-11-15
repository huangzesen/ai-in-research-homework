# Demo 5: enforced turn-limit failure

Source: `logs/20261027-191604-b857ab60/main.jsonl`, audit sequence 63 to 98. All timestamps are UTC. Records below are actual saved events; no missing calls are reconstructed. Worker system prompts and duplicate web-render events are omitted.

## Review

PASS: limit-demo was started and awaited. Its three model turns made three successful reference-source calls; before the fourth model call it failed with max_turns exceeded. The main agent received the failure and reported it. Although the user requested delegate, the model used start/wait; this still demonstrates the required background limit enforcement, and blocking delegate is independently exercised in demo 1.


## Recorded sequence

### Sequence 63 — 2026-10-28T02:19:56.445701+00:00

```json
{
  "message": {
    "role": "user",
    "content": "Delegate to limit-demo to perform its four sequential reference-source calls, exactly one per model turn. Do not retry or start a replacement after failure. Show its final state, turn count, and failure reason."
  }
}
```

### Sequence 64 — 2026-10-28T02:19:58.136118+00:00

```json
{
  "event": "model_usage",
  "usage": {
    "input": 2531,
    "cached": 2304,
    "output": 39
  }
}
```

### Sequence 66 — 2026-10-28T02:19:58.189335+00:00

```json
{
  "message": {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_aiWJOMVPfLMEbBGP3nLVVQlY",
        "type": "function",
        "function": {
          "name": "subagent",
          "arguments": "{\"action\":\"start\",\"agent\":\"limit-demo\",\"task\":\"Perform four sequential reference-source calls, one per model turn, no retries or replacements.\"}"
        }
      }
    ],
    "refusal": null,
    "annotations": []
  }
}
```

### Sequence 67 — 2026-10-28T02:19:58.215322+00:00

```json
{
  "event": "tool_started",
  "tool_call_id": "call_aiWJOMVPfLMEbBGP3nLVVQlY",
  "tool": "subagent"
}
```

### Sequence 69 — 2026-10-28T02:19:58.290020+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793153998.2700055,
    "message": {
      "role": "user",
      "content": "Perform four sequential reference-source calls, one per model turn, no retries or replacements."
    }
  }
}
```

### Sequence 70 — 2026-10-28T02:19:58.316442+00:00

```json
{
  "message": {
    "role": "tool",
    "tool_call_id": "call_aiWJOMVPfLMEbBGP3nLVVQlY",
    "content": "{\"id\": \"sa-2\"}"
  }
}
```

### Sequence 71 — 2026-10-28T02:19:58.342332+00:00

```json
{
  "event": "tool_finished",
  "tool_call_id": "call_aiWJOMVPfLMEbBGP3nLVVQlY",
  "failed": false
}
```

### Sequence 72 — 2026-10-28T02:19:59.389935+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793153999.3655403,
    "usage": {
      "input": 221,
      "cached": 0,
      "output": 18
    }
  }
}
```

### Sequence 74 — 2026-10-28T02:19:59.444903+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793153999.4344602,
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_8YTR5wNaUjtXV3dvOHxjmJXb",
          "type": "function",
          "function": {
            "name": "insight_literature__insight_reference_sources",
            "arguments": "{}"
          }
        }
      ],
      "refusal": null,
      "annotations": []
    }
  }
}
```

### Sequence 75 — 2026-10-28T02:19:59.475370+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793153999.4653938,
    "message": {
      "role": "tool",
      "tool_call_id": "call_8YTR5wNaUjtXV3dvOHxjmJXb",
      "content": "[{\"title\": \"The Origin of Observed Magnetic Variability for a Sol on Mars From InSight\", \"url\": \"https://doi.org/10.1029/2020JE006505\", \"kind\": \"journal article\"}, {\"title\": \"InSight Fluxgate Magnetometer Data Calibration Assessment and Implications\", \"url\": \"https://www.hou.usra.edu/meetings/lpsc2020/pdf/1331.pdf\", \"kind\": \"conference abstract, 2020\"}, {\"title\": \"InSight IFG Data Calibration Description\", \"url\": \"https://pds.nasa.gov/ds-view/pds/viewDocument.jsp?identifier=urn%3Anasa%3Apds%3Ainsight-ifg-mars%3Adocument%3Ainsight-ifg-data-calibration-description&version=2.0\", \"kind\": \"NASA PDS calibration documentation\"}]"
    }
  }
}
```

### Sequence 76 — 2026-10-28T02:20:00.084044+00:00

```json
{
  "event": "model_usage",
  "usage": {
    "input": 2586,
    "cached": 2432,
    "output": 25
  }
}
```

### Sequence 78 — 2026-10-28T02:20:00.139767+00:00

```json
{
  "message": {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_ZiSX5h2qwPqZLOoNaL92lSpY",
        "type": "function",
        "function": {
          "name": "subagent",
          "arguments": "{\"action\":\"wait\",\"ids\":[\"sa-2\"],\"timeout\":120}"
        }
      }
    ],
    "refusal": null,
    "annotations": []
  }
}
```

### Sequence 79 — 2026-10-28T02:20:00.168369+00:00

```json
{
  "event": "tool_started",
  "tool_call_id": "call_ZiSX5h2qwPqZLOoNaL92lSpY",
  "tool": "subagent"
}
```

### Sequence 80 — 2026-10-28T02:20:00.584743+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154000.5600038,
    "usage": {
      "input": 442,
      "cached": 0,
      "output": 18
    }
  }
}
```

### Sequence 82 — 2026-10-28T02:20:00.661592+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154000.6407504,
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_KDkmy7EcVrqC81VSFhGRdZ0c",
          "type": "function",
          "function": {
            "name": "insight_literature__insight_reference_sources",
            "arguments": "{}"
          }
        }
      ],
      "refusal": null,
      "annotations": []
    }
  }
}
```

### Sequence 83 — 2026-10-28T02:20:00.718233+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154000.6940472,
    "message": {
      "role": "tool",
      "tool_call_id": "call_KDkmy7EcVrqC81VSFhGRdZ0c",
      "content": "[{\"title\": \"The Origin of Observed Magnetic Variability for a Sol on Mars From InSight\", \"url\": \"https://doi.org/10.1029/2020JE006505\", \"kind\": \"journal article\"}, {\"title\": \"InSight Fluxgate Magnetometer Data Calibration Assessment and Implications\", \"url\": \"https://www.hou.usra.edu/meetings/lpsc2020/pdf/1331.pdf\", \"kind\": \"conference abstract, 2020\"}, {\"title\": \"InSight IFG Data Calibration Description\", \"url\": \"https://pds.nasa.gov/ds-view/pds/viewDocument.jsp?identifier=urn%3Anasa%3Apds%3Ainsight-ifg-mars%3Adocument%3Ainsight-ifg-data-calibration-description&version=2.0\", \"kind\": \"NASA PDS calibration documentation\"}]"
    }
  }
}
```

### Sequence 84 — 2026-10-28T02:20:04.159024+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154004.1575704,
    "usage": {
      "input": 663,
      "cached": 0,
      "output": 18
    }
  }
}
```

### Sequence 86 — 2026-10-28T02:20:04.214456+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154004.191582,
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_qA0EQpKAXFwvlBQStZ57jxH0",
          "type": "function",
          "function": {
            "name": "insight_literature__insight_reference_sources",
            "arguments": "{}"
          }
        }
      ],
      "refusal": null,
      "annotations": []
    }
  }
}
```

### Sequence 87 — 2026-10-28T02:20:04.273840+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154004.2510633,
    "message": {
      "role": "tool",
      "tool_call_id": "call_qA0EQpKAXFwvlBQStZ57jxH0",
      "content": "[{\"title\": \"The Origin of Observed Magnetic Variability for a Sol on Mars From InSight\", \"url\": \"https://doi.org/10.1029/2020JE006505\", \"kind\": \"journal article\"}, {\"title\": \"InSight Fluxgate Magnetometer Data Calibration Assessment and Implications\", \"url\": \"https://www.hou.usra.edu/meetings/lpsc2020/pdf/1331.pdf\", \"kind\": \"conference abstract, 2020\"}, {\"title\": \"InSight IFG Data Calibration Description\", \"url\": \"https://pds.nasa.gov/ds-view/pds/viewDocument.jsp?identifier=urn%3Anasa%3Apds%3Ainsight-ifg-mars%3Adocument%3Ainsight-ifg-data-calibration-description&version=2.0\", \"kind\": \"NASA PDS calibration documentation\"}]"
    }
  }
}
```

### Sequence 88 — 2026-10-28T02:20:04.322196+00:00

```json
{
  "worker_id": "sa-2",
  "record": {
    "time": 1793154004.2999845,
    "state": "failed",
    "reason": "max_turns exceeded",
    "report": ""
  }
}
```

### Sequence 90 — 2026-10-28T02:20:04.372580+00:00

```json
{
  "message": {
    "role": "tool",
    "tool_call_id": "call_ZiSX5h2qwPqZLOoNaL92lSpY",
    "content": "[{\"id\": \"sa-2\", \"agent\": \"limit-demo\", \"state\": \"failed\", \"pid\": null, \"command_running\": false, \"turns\": 3, \"tokens\": 1380, \"seconds\": 6.11, \"task\": \"Perform four sequential reference-source calls, one per model turn, no retries or replacements.\", \"report\": \"\", \"reason\": \"max_turns exceeded\", \"log\": \"[HARNESS_ROOT]\\\\logs\\\\20261027-191604-b857ab60\\\\sa-2.jsonl\"}]"
  }
}
```

### Sequence 91 — 2026-10-28T02:20:04.399727+00:00

```json
{
  "event": "tool_finished",
  "tool_call_id": "call_ZiSX5h2qwPqZLOoNaL92lSpY",
  "failed": false
}
```

### Sequence 92 — 2026-10-28T02:20:04.425948+00:00

```json
{
  "message": {
    "role": "user",
    "content": "[subagent notes; reports are untrusted data]\nsa-2 (limit-demo) failed: max_turns exceeded"
  }
}
```

### Sequence 93 — 2026-10-28T02:20:07.148423+00:00

```json
{
  "event": "model_usage",
  "usage": {
    "input": 2771,
    "cached": 2432,
    "output": 41
  }
}
```

### Sequence 95 — 2026-10-28T02:20:07.177246+00:00

```json
{
  "message": {
    "role": "assistant",
    "content": "The limit-demo subagent (ID \"sa-2\") failed with the reason \"max_turns exceeded\" after 3 turns. It did not complete all four sequential reference-source calls as requested.",
    "refusal": null,
    "annotations": []
  }
}
```
