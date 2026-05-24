# Tearsheet Return Audit - 2026-05-24

## Finding

The same backtest run could show different annualized return values across the HTML tear sheet, CSV artifact, and machine-readable JSON.

For the AITradingTeamStrategy run ending 2026-05-21, the HTML tear sheet showed roughly 190.96% total return and 581,694.55% annualized return, while another artifact path reported a different annualized return for the same run.

The mismatch came from two separate bugs:

- QuantStats Lumi `reports.html(..., match_dates=False)` still called `metrics()` with the default `match_dates=True`, so the HTML summary could silently drop the explicit anchor/first strategy return while `metrics_json()` kept it.
- Lumibot merged strategy and benchmark rows before daily resampling, so a later benchmark-only timestamp could win `.last()` for a day and erase that day's strategy move.

With both fixes applied, the saved run rerenders at 194% total return and 633,949.78% annualized return in the HTML/CSV display, while `tearsheet_metrics.json` reports the same values as raw decimals (`1.94` total return and `6339.4978` CAGR).

## Fix Direction

- QuantStats Lumi should format display metrics with thousands separators in both summary cards and the Key Performance Metrics table.
- Parameters should render as a full-width bottom section so long parameter names and values can wrap.
- Lumibot should not recompute or rewrite QuantStats headline metrics after the HTML has already been rendered.
- Lumibot HTML, CSV, and metrics JSON generation should use the same `match_dates=False` convention so all artifacts agree.

## Related GitHub Issues

- Lumiwealth/quantstats_lumi#77: trading days/year annualization discussion.
- Lumiwealth/quantstats_lumi#74: open PR to change CAGR years calculation.
- Lumiwealth/quantstats_lumi#81: max drawdown first-return edge case.
- Lumiwealth/quantstats_lumi#30 and #44: Sharpe/Sortino annualization period discussion.
