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

## Named rows

- The monthly downside row is named `Worst 1-Month Return`.
- `Worst Month` is no longer the canonical tearsheet row name.

## Known row-level normalization

`Percent Positive Months` is semantically percentage-like but appears without `%`
in the current internal metrics table output. It is normalized to raw decimal in
`metrics_json` (`83.33` -> `0.8333`).

## Custom metrics

- Custom metrics are merged into `scalar_metrics` exactly once, after built-in tearsheet rows are collected.
- Custom metric values must be machine-typed scalars (`int`, `float`, `bool`, `string`, or `"-"` for unavailable).
- For the cleanest HTML/JSON parity, prefer scalar custom metrics:

  ```json
  {
    "Custom Return Observation Count": 252,
    "Custom Mean Absolute Daily Return": 0.0117
  }
  ```

- Nested custom metric dicts are supported, but if you want exact key parity between HTML and JSON, return explicit display column names rather than convenience aliases:

  ```python
  {
      "Custom Relative Edge": {
          "Strategy": 1.23,
          "Benchmark (SPY)": 0.91,
      }
  }
  ```

- Custom metrics are treated as literal scalars. They do not receive automatic percent/unit conversion.

## Strict JSON

- `metrics_json(..., output=...)` must always write strict RFC-compatible JSON.
- Raw `NaN`, `Infinity`, and `-Infinity` values are never allowed in output files.
- Non-finite numeric values inside nested tables, arrays, pandas objects, or drawdown summaries are recursively sanitized before writing.
- JSON writes use `allow_nan=False` so missed non-finite values fail in tests instead of silently creating invalid artifacts.

## Guardrails

Regression tests in `tests/test_reports.py` enforce:

- key metric parity against internal tearsheet rows,
- no `%` strings in `scalar_metrics` values,
- raw-decimal output for risk-free rate and percent-positive-months rows,
- inclusion of `Worst 1-Month Return` in the full tearsheet metrics table,
- numeric custom metric preservation in `summary_only` JSON output,
- strict JSON output with recursive non-finite value sanitization.
