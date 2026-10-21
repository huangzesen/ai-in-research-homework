---
name: psp-data
description: Use for questions about Parker Solar Probe (PSP) measurements, such as solar wind speed, density, temperature, magnetic field or distance from the Sun at a given time or perihelion. Explains which psp tool to call, PSP conventions (RTN, units, perihelion dates) and the data caveats to mention.
---

# Parker Solar Probe data (CDAWeb)

## Which tool

1. **`psp__solar_wind_summary(start, stop)`** first, for almost any "what was the solar wind like at PSP..." question. One call returns speed, density, temperature, distance from the Sun and |B| with times of extremes, and saves CSVs.
2. **`psp__describe_cdaweb_dataset(dataset_id)`** to see a dataset's parameters and coverage.
3. **`psp__get_cdaweb_data(dataset_id, parameters, start, stop)`** for anything else (other parameters or datasets, e.g. `OMNI_HRO_1MIN` for near-Earth comparison).

Times are UTC, ISO 8601 (`2024-12-24` or `2024-12-24T06:00`); at most 7 days per call. For "near perihelion N", use a window of about 1 day centered on that perihelion; the closest approach time is in the summary's distance line, so you can confirm it from the data.

## Perihelion dates (UTC, approximate; confirm with the distance line)

- Perihelia 22, 23, 24: 2024-12-24, 2025-03-22, 2025-06-19 (closest, about 9.9 R_sun, 0.046 AU).
- For other encounters, ask the user, or scan a few days with `solar_wind_summary` and read the minimum distance.

## Conventions an agent wouldn't know

- **RTN**: R points from the Sun to the spacecraft (radially outward), T is roughly along the planets' orbital motion, N completes the right-handed set. "Solar wind speed" usually means the radial speed Vr; also report |V| if it differs a lot.
- **Units**: density in cm^-3, speed in km/s, temperature reported in K (SPAN-i gives eV; 1 eV = 11,604.5 K), B in nT, distance in solar radii (1 R_sun = 695,700 km) and AU.
- **Br sign** tells the magnetic sector: Br > 0 field points away from the Sun, Br < 0 toward it. A brief flip in Br (with a spike in Vr) is a switchback.

## Caveats to mention when relevant

- **SPAN-i gives partial moments.** Its field of view is partly blocked by the heat shield, so when the proton beam is outside it (more common far from the Sun and in early encounters), density can be underestimated and speed biased. Say so if a density looks low.
- **Quality flags**: `QUALITY_FLAG` is a set of bit flags, and nonzero values are common and often informational, so don't call data bad just because the flag is nonzero. The summary lists the most common values; if the user needs a strict selection, point them to the SWEAP data documentation and the saved CSV.
- **Outliers**: prefer the median and the 5 to 95% range over min and max, which single bad samples or switchbacks can set. Non-positive densities and temperatures are already dropped.
- **Data gaps**: PSP sends data down weeks to months after an encounter, and FIELDS and SWEAP don't always cover the same times. "No data" usually means not yet released or outside an encounter.
- Give numbers with sensible precision (e.g. "about 350 km/s"), and the time window you used.

## Replying on a phone

Lead with the answer in one or two sentences, then at most 3 to 4 short lines of supporting numbers. Mention the saved CSV path only if the user wants the full data.
