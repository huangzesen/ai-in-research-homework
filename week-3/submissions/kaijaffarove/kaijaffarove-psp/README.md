# kaijaffarove-psp

An MCP server, packaged as a Claude Code plugin, that answers questions about **Parker Solar Probe** measurements using NASA's public [CDAWeb HAPI service](https://cdaweb.gsfc.nasa.gov/hapi). Read-only; no API key.

## Tools

| Tool | What it does |
|---|---|
| `solar_wind_summary(start, stop)` | SWEAP/SPAN-i proton moments (`PSP_SWP_SPI_SF00_L3_MOM`) plus FIELDS 1-minute B (`PSP_FLD_L2_MAG_RTN_1MIN`): median, mean, min and max (with times) of radial speed, speed, density, temperature, distance from the Sun, \|B\| and Br, plus a quality-flag count. Saves both tables as CSV. |
| `describe_cdaweb_dataset(dataset_id)` | Time coverage and parameters (names, units, sizes) of any CDAWeb dataset. |
| `get_cdaweb_data(dataset_id, parameters, start, stop)` | Any parameters of any CDAWeb dataset: statistics per column, full table saved as CSV. |

Times are UTC ISO 8601 (`2024-12-24`, `2024-12-24T06:00`), at most 7 days per call. Tools return short text; full tables go to `PSP_DATA_DIR` (default `~/psp_data`). Errors say what to try next.

The skill `skills/psp-data/SKILL.md` tells an agent which tool to use, PSP conventions (RTN, units, perihelion dates) and data caveats (SPAN-i partial moments, quality flags, gaps).

## Configure

Nothing required. Optional: `PSP_DATA_DIR` for where CSVs are saved. Requires [uv](https://docs.astral.sh/uv/) (it installs `mcp` and `httpx` automatically) and internet access to cdaweb.gsfc.nasa.gov.

## Load it

- **kai-agent** (https://github.com/kaijaffarove/kai-agent): loads every folder in `plugins/` automatically.
- **Claude Code**: `claude --plugin-dir path/to/kaijaffarove-psp`, then `/mcp` lists `psp`. Ask e.g. "What was the solar wind speed at PSP around perihelion 22 (2024-12-24)?"

## Data credit

PSP SWEAP (Kasper et al. 2016) and FIELDS (Bale et al. 2016) data via NASA's Space Physics Data Facility CDAWeb.
