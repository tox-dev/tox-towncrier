# Where to Look First

When picking up a task, get oriented before proposing anything.
Read, in this order:

1. The packaging metadata -- what the project is, what it depends
   on, what it exposes.
2. The source of the module the task is about.
3. The shared test fixtures, then the tests for that module --
   they are the behavioral contract.
4. `tox.ini` and `.pre-commit-config.yaml` -- how things get run
   locally and in CI.
5. The main CI/CD workflow.

Here:

1. `pyproject.toml` (build backend, metadata, and the `tox`
   entry point).
2. `src/tox_plugins/towncrier/_plugin.py` -- the entire plugin.
3. `tests/conftest.py` (loads `tox.pytest`, isolates the user's
   tox config), then `tests/integration_test.py`.
4. As above.
5. `.github/workflows/ci-cd.yml`, which delegates to
   `tox-dev/workflow`'s `reusable-tox.yml`.

Other places worth knowing:

- `.github/reusables/tox-dev/workflow/` -- the hook actions
  `reusable-tox.yml` calls into.
- `.github/actions/cache-keys/` -- a composite action computing
  cache keys.
- `.github/SECURITY.md`, `.github/THREAT_MODEL.md`,
  `.github/INCIDENT_RESPONSE.md` -- the security policy docs.
