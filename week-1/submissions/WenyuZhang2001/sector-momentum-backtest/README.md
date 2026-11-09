# Audit industry strategies against ordinary investment alternatives

**Author:** Wenyu Zhang · **Field:** quantitative finance · **Status:** independent final review passed (`solvable`, 2026-11-08); awaiting student instruction/window/publication approvals and course integration checks.

The task evaluates three supplied, frozen industry policies against passive market and short-term T-bill return proxies, under matched upfront and monthly contributions, with CPI purchasing power and contribution-neutral drawdown. All historical audit inputs are supplied; no proprietary investment-bank strategy is needed. Passing means a correct audit, including negative findings, rather than a mandatory profitable outcome.

## Difficulty

The scientific pitfalls are mistaking new contributions for returns, annual interest quotes for daily returns, risk-taking for investment skill, nominal gains for purchasing-power gains, or retrospective results for future guarantees. A pipeline error propagates into the quarterly comparisons and final conclusions. This is an accounting and research-audit task, not yet demonstrated to be difficult for a frontier model. The retained 1.5-hour expert estimate is provisional, not an evidence-backed year of research. No years-long difficulty or model failure is claimed. A broader quantitative research problem would be needed to establish that ambition honestly.

## Reference solution

`solution/solve.py` and `analysis.py` compute the audit directly from public inputs. They do not import tests/authoring or copy expected outcomes. Each policy receives only prior completed-day industry returns, capped at 1,260 days. Dollar holdings include costs; every scenario matches contribution amounts/dates; final CPI is used only for retrospective purchasing-power evaluation. New contributions issue NAV units, so they cannot conceal drawdown.

The three strategy sources are supplied inputs from the earlier exploratory author study, not an unbiased selection from a pristine holdout. They are fixed for this task, and no new fitting is allowed. `authoring/daily-prototype/` preserves the development and negative results; `authoring/legacy-monthly-a/` preserves the earlier monthly task prototype.

## Verification

### 你正在确认什么（中文评分规则）

这次评分判断的是“分析是否算对”，不是“策略是否赚钱”。即使结论是策略没有优势，只要数据、计算和比较结论都正确，也可以通过；只写“更好”或“不好”不能通过。

**必须交齐两份答案：**

1. 季度明细表 `quarterly_comparison.csv`：必须恰好有160条不重复的记录，即2种投入方式 × 5种方法 × 16个季度，不能漏掉表现差的季度。每条都要包含题目规定的本金、期末资产、费用、通胀保值金额、购买力变化、最大回撤及胜负标记。
2. 汇总表 `summary.json`：必须列出每种方法在每种投入方式下的胜场数、平均期末资产、平均购买力变化、最差季度回撤、总费用和比较结论，字段名和类型按题目要求填写。

**哪些计算必须正确：**

- 投入必须公平：一次投入场景都在季初收到全部本金；按月投入场景都在每个月首个交易日收到1/3本金。第二、三个月的钱不能提前拿来投资，新增本金不能算成投资收益。
- 费用必须计算：股票策略和大盘按题目规定扣交易和季度末清仓费用；短债代理按题目约定不扣费用。不能漏扣，也不能随意换费率。
- 通胀必须按题目指定的CPI月份计算，不能把名义赚钱直接当作购买力增长。短债收益使用每日RF，不能把年利率直接当成日收益。
- 回撤要排除追加本金的影响，并包括清仓费用；用负数表示。例如，-25%的跌幅比-20%更大，不能反过来说更稳健。
- 每个季度的收益、费用、通胀、回撤和标记都会核对，不能只让最后的平均数看起来正确。

**“赢”和“多数季度”的确切含义：**

- 与大盘、短债或通胀保值金额比较时，期末资产必须高出对应金额超过0.0000000001，才计为赢；相同不计为赢。金额单位是季度总投入本金为1。
- 联合胜场要求同一季度同时超过大盘、短债和通胀保值金额，不能分别挑不同季度相加。
- 16个季度中至少赢9个，才算“多数季度”；赢8个不算。胜场数和这些判断必须完全正确，不接受“大约9个”。
- 比较回撤时，按同一投入方式下最差季度的回撤判断更大、更小或相同；这些是历史描述，不代表未来保证或统计显著性。

**允许多大的数值误差：**

- 收益、资产、费用等小数允许相对误差0.00000001，或绝对误差0.0000000001，满足任意一个即可。例如某项参考结果假设为0.10，算成0.1000000005可以接受，算成0.11不能接受。这里的数字只是解释误差规则，不是本题答案。
- 允许这点误差，是因为不同计算工具可能有末位舍入差异；同一批固定数据并没有要求估计未知未来收益。胜场数、文字标签和真假判断不采用这个小数容差。
- 季度记录顺序可以不同，但列顺序按题目要求；汇总字段不得缺失或随意增加。空白、无穷大、NaN、重复记录或缺失记录不合格。两份文件各不得超过2MB，正常答案远小于这个限制。

**最后怎样给分：**

季度明细检查和汇总检查必须同时通过，才得1分；任何一项失败都得0分。两项检查不是各占一半，不按收益高低额外加分，也不要求使用和参考分析相同的代码。

### Validation evidence / 验证依据

The separate offline verifier reads only the two submitted artifacts. `authoring/evidence/calibrate.py` tests an isolated reference, reconciles all 160 rows with the prior pipeline, and recomputes zero-cost, ignored-inflation and premature-contribution mistakes. Correct reference outputs pass; no-op, wrong accounting and constant-negative claims fail. The independent final review reproduced all 160 account rows, accepted row reordering and 12-significant-digit rounding, and rejected malformed or numerically incorrect outputs. The numeric tolerance is relative 1e-8 or absolute 1e-10; this is arithmetic reproducibility, not statistical confidence or investment merit. See `authoring/solvability.md` and `authoring/evidence/calibration.json`. Full Docker/Harbor integration has not been run locally.

## Data and limitations

Daily industry/market/RF observations: French December 2024 legacy archive, exported as decimals for 2009–2024. CPI: BLS CPI-U all-items US city average, monthly unadjusted, via FRED, December 2008–December 2024. See authoring/provenance/data_sources.md and audit_input_hashes.json. Source policy provenance is recorded there. Inputs are historical and already inspected; the task makes no secret/prospective-data claim.

Market means the French broad U.S. equity return, not S&P 500 or Nasdaq; it is not principal-stable. RF is a frictionless one-month T-bill proxy, not a bond-ladder execution model. Industry portfolios are research returns, with idealized prior-close fills and no taxes or additional impact. CPI endpoints use monthly averages. The sixteen scoring quarters are a small retrospective sample. Better observed returns cannot establish lower risk, statistical significance or future superiority.

## Status and next steps

Student approved the exact instruction in their own terminal. The numeric-window and publication approvals remain pending. The current authoring/solvability.md independently reviewed this historical-audit version and returned solvable. The reviewer recomputed all 160 rows with a separate account loop (maximum absolute difference 2.22e-16), checked source exports and demonstrated rejection of wrong outputs. This confirms the deterministic task contract, not research hardness or investment merit. No Week 6 push, PR, full container run or frontier-model result is claimed.
