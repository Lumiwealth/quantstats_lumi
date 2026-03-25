# DEPLOYMENT

## Release model

`quantstats_lumi` now uses the same tag-driven deployment model as `lumibot`:

1. Push release branch changes.
2. Tag the release commit as `vX.Y.Z`.
3. Push tag.
4. GitHub Actions validates tests/build, publishes to PyPI, and creates GitHub release notes.

Workflow file:

- `.github/workflows/python-publish.yml`

## Release order for tearsheet metric changes

When tearsheet metrics change, the release order is strict:

1. Update and release `quantstats_lumi` first.
2. Update downstream consumers (for example `lumibot`) to require the new minimum version.
3. Validate a clean environment using the released QuantStats package plus the updated downstream consumer source.
4. Only then release the downstream consumer.

This avoids mixed-version tearsheet behavior and stale local validation.

## Downstream dependency policy

For the current tearsheet metrics contract, downstream consumers should require:

```text
quantstats-lumi>=1.1.3,<1.2.0
```

## Required secret

The release workflow expects:

- `PYPI_API_TOKEN` in GitHub Environment: `pypi`

## Local secret bootstrap (recommended)

1. Copy template:

   ```bash
   cp .env.release.local.example .env.release.local
   ```

2. Fill `.env.release.local` with your real `PYPI_API_TOKEN`.

3. Sync to GitHub:

   ```bash
   ./scripts/sync_release_secrets.sh
   ```

## Verify release

After tag push, verify:

```bash
gh run list -R Lumiwealth/quantstats_lumi -L 5
python3 -m pip index versions quantstats-lumi | head
```
