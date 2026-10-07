# Lunar crater chronology: formation and resurfacing ages from a CSFD

**Author:** Patrick Russell (UCLA) · **Field:** planetary science / lunar crater chronology · **Class level:** 1 · **Agent budget:** 2 h

The solver gets a raw crater catalogue (about 105,000 craters, 400,000 km²) for a synthetic lunar geologic unit and must write the unit's formation model age, the age of a later resurfacing event, and the diameter range used for the formation age, using the Neukum et al. (2001) production and chronology functions.

## Difficulty

Crater-count dating looks like "fit one age", but the answer depends on judgments an expert learns over months. Below about 1 km the catalogue is contaminated by steep-sloped secondary craters, and below about 0.3 km it is incomplete, so the small-D counts cannot be trusted. Craters smaller than about 3 km record a younger resurfacing event while larger craters record the formation age, so one age fitted to everything is wrong (it gives about 1.9 Ga when the formation age is 3.55 Ga). The solver must find the kink and the clean fit ranges itself, and must handle the production function correctly: cumulative vs. differential counts, and the corrected linear term of the chronology function (10^a0, not the typo in the printed paper). The catalogue is synthetic, drawn from the Neukum production function so the truth is known; real CSFD work has the same pitfalls plus mapping and geology judgments.

## Reference solution

`solution/solve.py` drops D < 1 km (secondaries, incompleteness), bins the rest in log-spaced diameter bins, and scans for the diameter where the model age steps from younger to older by maximizing a Poisson likelihood. At each step location the best-fit age of each segment is the one whose expected Neukum count equals the observed count. It reports the old-segment age, the young-segment age and the old segment's diameter range. The data generator is in `authoring/provenance/generate_data.py` (fixed seed) and the production function code is in `solution/neukum.py`.

## Verification

`tests/test_outputs.py` checks that `answer.json` parses with the required keys, that `age_ga` is within ±0.15 Ga of the true 3.55 Ga, that `resurfacing_age_ga` is within ±0.25 Ga of the true 1.85 Ga, that the resurfacing is younger than the formation, and that the formation fit range lies at or above 2.5 km (above the ~3 km resurfacing cutoff) and spans at least a factor of two. The formation-age window (±0.15 Ga) is wider than the Poisson scatter of the fit (about ±0.05 Ga from 82 large craters), and every reasonable choice of fit range above the kink (D ≥ 3, 3.5 or 5 km) lands inside it (3.55, 3.53, 3.58 Ga), as does using the typo'd chronology constant (3.55 Ga). A fit that starts at 2 km mixes in young craters and gives 3.25 Ga, which fails. The resurfacing window is wider (±0.25 Ga) because only a few hundred craters in a narrow diameter range constrain it (Poisson scatter about ±0.08 Ga) and fit-range choices matter more: fitting 1–3 km gives 1.69 Ga and 0.7–3 km gives 1.90 Ga, and both pass. A single age fitted to all D ≥ 1 km gives 1.88 Ga for the main age and fails, so the task cannot be passed by ignoring the resurfacing. A weakness at level 1: an agent that guesses typical lunar surface ages (about 3.6 and about 2 Ga) could land in both windows by chance, though the fit-range check and the need to write consistent values make this unlikely; level 2 should calibrate this with a script.

## Attempts

See `authoring/attempts.md`.
