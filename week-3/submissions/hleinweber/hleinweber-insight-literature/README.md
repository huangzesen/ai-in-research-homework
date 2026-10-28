# InSight literature plugin

Read-only literature discovery for InSight seismology, Mars interior structure, and fluxgate magnetometer interference/calibration. No API key or private data is needed.

## Tools

- `search_papers`: Crossref title search, optional inclusive year bounds, and 1-10 results. For multiple requested interior regions it runs separate title queries and prioritizes matching titles. It scans the first 50 matches per query and filters for mission terms; magnetic queries also require magnetic terms. This is not a full-text or exhaustive search.
- `get_paper`: DOI metadata and unverified deposited text. Suspected shared editorial summaries are flagged and withheld entirely; findings_supported is false and required_action requests a primary source; missing metadata does not imply the paper lacks an abstract or uncertainties. Verify exact titles, years and publication types before citing.
- `insight_reference_sources`: fixed magnetic-calibration starting links to an article, conference abstract and NASA PDS documentation; not a seismology bibliography.

Requires uv and Python 3.11+. The uv script declares the official MCP Python SDK dependency with a <2 bound. Network calls time out after 20 seconds. Crossref metadata can be incomplete or have unexpected dates. Relevance and scientific claims require source review, even after DOI verification.

## Load

In Claude Code, from the harness root:

```sh
claude --plugin-dir plugins/hleinweber-insight-literature
```

In the research-agent harness, keep this folder under `plugins/` and run `uv --system-certs run python agent.py` or `uv --system-certs run python agent.py --telegram`. The loader expands `${CLAUDE_PLUGIN_ROOT}` in `.mcp.json`. Read-only tools are allowed in the harness's `settings.json`.

Any MCP stdio client can run `uv run --script /absolute/path/server.py`. The server writes protocol messages to stdout; keep diagnostic logging on stderr.

Try: Find papers using InSight seismic observations to constrain Mars's crust and core. Verify each DOI, distinguish radio tracking from seismology, and label conference material and reviews.

The skill covers seismology and magnetic calibration. It warns about editorial summaries describing multiple companion papers. Metadata/abstract retrieval is not a full-paper review, and citation instructions are not a programmatic guarantee.

## Validation status

Live SDK discovery, search, DOI lookup, source listing and invalid-input checks passed. The student observed search and DOI tool calls and received research answers over Telegram. Exact metadata for the 2021 core and crust papers was verified; scientific summaries still require review. Codex host validation passed for search, curated sources and DOI lookup. Final live SDK checks also passed for all three tools and invalid inputs.


Scientific accuracy follow-up: a phone test initially mixed findings from a shared Science editorial summary into individual papers. The tool now withholds suspected editorial text and marks findings unsupported; multi-region searches alternate crust/core results. Live checks returned the central 2021 crust and core papers first and withheld editorial text for all three Science DOIs. The student repeated the original question after restart: correct key citations and DOI links were returned, and unsupported findings for those papers were withheld. This verifies citation discovery and evidence handling, not a complete scientific synthesis: extra results still included indirect geological/modeling studies, and the blanket observation-method claim was too broad. Primary-source review remains necessary for findings, uncertainties and method attribution. No full-paper retrieval is implemented.

Crossref API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
