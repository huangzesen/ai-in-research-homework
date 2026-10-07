# Monthly industry-momentum portfolio backtest

**Author:** Wenyu Zhang (UCLA) · **Field:** quantitative finance · **Class level:** 1 · **Agent budget:** 60 min

The solver receives frozen monthly industry returns and market factors from the Kenneth R. French Data Library. It must backtest the specified top-three industry-momentum strategy with turnover costs, compare it with the market, and report monthly results plus full-sample and holdout metrics.

## Difficulty

The challenge is implementing timing and accounting conventions consistently: the signal skips the most recent month, holdings drift before rebalancing, turnover counts both buys and sells, and costs affect compounded net returns. A quantitative researcher would use this workflow to evaluate a portfolio rule before deciding whether it merits further study. The inputs are real historical research returns from a public archive; the portfolio is a specified research construction, not a record of executable ETF trades.

## Reference solution

The reference solution parses the monthly value-weighted industry table and the market and risk-free factor series, converts percentages to decimal returns, and computes the 11-month signal with a one-month skip. It selects the three strongest industries, applies equal target weights after accounting for drift and transaction costs, then computes compounded wealth and risk metrics for the complete sample and the fixed 2000–2024 holdout.

## Verification

The verifier checks all 1,170 monthly rows, including the selected industries, weights, turnover, costs, and returns; each monthly numeric value is accepted within 1e-8 absolute error. This tolerance allows small rounding and implementation differences while remaining tight enough to reject materially different monthly results. Summary metrics are accepted within 1e-8 relative or 1e-10 absolute error. The strategy conventions and archive vintage are fixed; a no-op agent and an output with a corrupted monthly return both fail the verifier.

## Attempts

See `authoring/attempts.md`.
