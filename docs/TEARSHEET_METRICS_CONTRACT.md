# Tearsheet Metrics JSON Contract

`tearsheet_metrics.json` (`metrics_json(..., summary_only=True)`) is the canonical
machine-readable tearsheet summary payload.

## Contract

- `scalar_metrics` values must be machine-typed (`number`, `string`, `null`-like `"-"`), not display-formatted `%` strings.
- Percentage-style metrics must be exported as raw decimals:
  - `7%` -> `0.07`
  - `-1.86%` -> `-0.0186`
  - `3.69%` -> `0.0369`
- Ratio/coefficient metrics stay as raw numeric ratios (no extra scaling):
  - Sharpe, Sortino, RoMaD, Calmar, Omega, Corr to Benchmark.
- Count/day metrics stay numeric counts:
  - Longest DD Days, Avg. Drawdown Days, Time to Recovery (Days), Time Underwater (Days).
- Date/name metadata rows remain strings:
  - Start Period, End Period.

## Known row-level normalization

`Percent Positive Months` is semantically percentage-like but appears without `%`
in the current internal metrics table output. It is normalized to raw decimal in
`metrics_json` (`83.33` -> `0.8333`).

## Guardrails

Regression tests in `tests/test_reports.py` enforce:

- key metric parity against internal tearsheet rows,
- no `%` strings in `scalar_metrics` values,
- raw-decimal output for risk-free rate and percent-positive-months rows.
