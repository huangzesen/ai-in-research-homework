# Expanded investment comparison — candidate measurement framework

The owner requested inflation, periodic investment and stable-interest comparisons. The existing primary goal remains quarterly wins against the market. The additional measures below are evaluated descriptively; they do not silently change rewards, passing hurdles or the previously selected strategies.

## What each comparison answers

- Broad market total return: does the strategy outperform passive equity exposure after prescribed costs? The existing French benchmark is not S&P 500/Nasdaq and is not a guaranteed or principal-stable investment.
- One-month T-bill RF proxy: does the extra risk earn more than the dataset’s short-term interest alternative? Compound the actual daily RF observations. Do not divide an annual quoted yield by 252 or confuse it with a long-bond price return. RF is taken from the same December 2024 archive; it is a frictionless proxy, not an executable bond ladder.
- CPI purchasing power: does final wealth preserve the purchasing power of each contribution? Use BLS CPI-U all-items US city average, not seasonally adjusted, distributed as FRED CPIAUCNS. Grade with monthly endpoint proxies. No daily CPI is fabricated, and CPI is used only ex post, not as a strategy signal. Uniform deflation does not change same-period portfolio rankings.
- Periodic investment: this is a cash-flow schedule, not an asset. In the monthly scenario, all compared accounts receive 1/3 of the quarter’s total capital on each first trading day. No account receives future contributions early. Market buys these installments immediately; strategy and RF receive exactly the same amounts and dates. This is compared separately from the lump-sum scenario. We do not compare raw ending wealth across scenarios to claim a strategy effect.
- Risk: report maximum drawdown of a unitized NAV that removes contributions, so new money cannot mask losses. Report trading fees. Return superiority does not imply equivalent or lower risk.

## Definitions and measurements

All quarters use total contributed capital 1, daily decisions, the existing idealized close-to-close industry-return convention and 10 bp traded-notional costs for strategy/market. Both risky portfolios liquidate at quarter end. The RF proxy is assumed frictionless and remains cashlike; this favors the conservative comparator and is disclosed. Capital is reset each quarter, observations are not.

Purchasing-power hurdle is sum(contribution * CPI_end / CPI_prior_month_at_deposit). The end index is the quarter-end month average; each contribution uses its preceding month average. These are period approximations, not exact daily consumer prices. The ratio of final wealth to this hurdle minus 1 is a contribution-weighted purchasing-power gain, not an annualized return, time-weighted return or IRR.

Joint wins count quarters when terminal wealth exceeds market wealth, RF wealth and the inflation-preserving hurdle by more than 1e-10, under identical cash flows. This is an additional descriptive metric, not an approved new pass rule. It does not by itself exclude static industry shortcuts. A risk gate would require a separate owner decision and calibration; do not require equity risk to match a near-zero-volatility RF proxy.

## What the current evidence shows

Across 2021–2024 (16 quarters), the frozen rule has 9 joint wins with lump-sum and 8 with monthly contributions; the learned model has 3 and 1. Equal industry weighting has 3 and 3; the explicitly hindsight financial-industry baseline has 6 and 4. Thus the new measures change interpretation but do not establish research difficulty or generalizable skill.

The frozen rule’s worst unitized quarterly drawdown in the lump-sum scenario is about -25.83%, versus about -21.05% for the market. It cannot be described as uniformly safer than market holding. Final observations were already inspected; no statistical or future-performance superiority is claimed.

See evidence/benchmark_comparison.json for every quarter and exact metrics, evidence/benchmark_validation.json for checks, and benchmark-data/provenance.json for source metadata. The old lump-sum wealth outcomes were reproduced for all four methods; every scenario has matched contributions; passive market/RF wealth was independently recomputed for each quarter. CPI coverage is complete through December 2024. No strategy was refitted or selected using these additional comparisons.

## Sources

- CPI definition and data: https://fred.stlouisfed.org/series/CPIAUCNS and https://www.bls.gov/cpi/questions-and-answers.htm
- RF/market series definition: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html
- Periodic-investment definition: https://www.investor.gov/introduction-investing/investing-basics/glossary/dollar-cost-averaging
- Equity risk context: https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks
