# DEPLOYMENT

## Release model

`quantstats_lumi` now uses the same tag-driven deployment model as `lumibot`:

1. Push release branch changes.
2. Tag the release commit as `vX.Y.Z`.
3. Push tag.
4. GitHub Actions validates tests/build, publishes to PyPI, and creates GitHub release notes.

Workflow file:

- `.github/workflows/python-publish.yml`

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
