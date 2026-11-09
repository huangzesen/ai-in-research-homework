# Research checkpoint: quarterly win rate after 2008

Data: official French December 2024 daily archive, ending 2024-12-31. Development uses 2009–2016, with 2009–2010 warming up long windows; validation uses 2017–2020; final retrospective scoring uses 2021–2024 (16 quarters). Primary objective is quarterly wins after stated costs, with daily changes allowed. Benchmark is French broad U.S. market, not S&P 500 or Nasdaq. Historical training/validation market data are now disclosed with owner agreement; final-period market and industry outcomes are withheld from the strategy source.

| Method | Validation wins vs market | Final wins vs market |
|---|---:|---:|
| Fixed-rule family selected on market target: constant BusEq | 14/16 | 9/16 |
| Learned linear-score family, selected within six variants | 10/16 | 4/16 |
| Daily equal weight | See full calibration records | 7/16 |
| Best observed final single-industry baseline: Money | Not used to select this baseline | 10/16 |

The static-policy result is reused from the byte-identical prior frozen source. The learned family is one additional exploratory final replay, with source and selection records saved before scoring. No data were changed and no failed method was removed. The training/validation winner is not necessarily the best final-period policy, and using that final winner to choose a future method would be hindsight.

Training-target alignment was necessary for a coherent experiment, but did not establish a strategy with a research advantage. A 45-rule family and one six-model learned family are limited searches; their failures do not prove no better strategy exists. Conversely, simple static holdings passing a low hurdle do not demonstrate deep scientific reasoning. No binary threshold is justified yet, and no successful hard reference is claimed. Avoid further grading-period-guided model search. A material scientific design decision is needed before publication as a research benchmark.

Execution limitations: idealized prior-close fills, industry research returns rather than executable securities, assumed 10 bp turnover/entry/exit costs, and no taxes or additional slippage. Final observations were inspected during previous experiments and are not pristine. Sixteen final quarters give coarse win rates; no statistical or future-performance guarantee follows. Full Docker/Harbor integration remains untested.

## Threshold sensitivity (descriptive, no new grading rule)

A round is counted only when quarterly net strategy return minus net market return exceeds the stated percentage-point threshold plus 1e-10. This is not a relative return increase or wealth multiple. All 16 saved quarterly outcomes are reused, without model fitting or rescoring from changed data. Thresholds examined: 0, 1, 2, 5, 10, 20, 50 and 100 percentage points.

At 0 pp, the frozen rule/learned strategies win 9/4 quarters. At 5 pp they win 3/2, at 10 pp 1/0, and at 20, 50 and 100 pp both win zero. At 20 pp, constant Durbl and Enrgy each win two rounds; at 50 and 100 pp none of the twelve static industries wins a round. Raising thresholds does not by itself isolate research skill. These limited tested policies do not prove that a better strategy is impossible. The best-static curve chooses its maximum separately at each threshold after seeing final outcomes, and is explicitly a hindsight diagnostic, not one implementable selected rule.

Full per-method counts and min/median/max excess returns are in evidence/threshold_sensitivity.json and threshold_counts.csv. All count calculations were independently checked with Decimal wealth subtraction, matched to the stored base wins, and checked for monotonicity and quarter/benchmark alignment. These are exploratory checks on previously inspected historical outcomes; no pass threshold or reward has been changed. The inline chart rows match these values; the host Node chart validator was unavailable and rendering was not inspected.
