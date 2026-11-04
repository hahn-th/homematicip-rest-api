# Contributing

## Reporting a device that is missing or incomplete

The maintainers do not own most of the hardware. A configuration dump is what makes a device
implementable without it, so attach one to the issue: `hmip_cli --dump-configuration
--anonymize`, or the diagnostics download of the Home Assistant integration. Name the model as
printed on the device and say what it should do that the library cannot do yet.

## Pull requests

- Every change comes with tests. Fixtures live under `tests/` and the fake cloud server in
  `homematicip_demo/` serves `homematicip_demo/json_data/home.json`, so a new device or channel
  is added there from a real dump and tested against it.
- Add an entry to `CHANGELOG.md` under `UNRELEASED`, in the section it belongs to (Added,
  Changed, Fixed, Removed). Write it for the user of the library: what changed and why, with the
  issue number when there is one.
- A new device gets its line ticked, or added, in the device list of `README.md` in the same
  pull request. The list is what people search before opening an issue.
- Run `ruff check src tests` and `pytest` before pushing; the CI runs both on Python 3.12,
  3.13 and 3.14.
- Keep a pull request to one change. Small ones get merged, mixed ones wait.

## Development setup

```sh
pip install -e .
pip install -r requirements_dev.txt
pytest
```

`make docs` builds the documentation site into `site/`, `make serve` runs it locally. Both
copy `README.md` and `CHANGELOG.md` into `docs/` and generate the API reference from the
docstrings, so edit the originals, not the copies.

## Releases

Releases are cut from `master` by the maintainers: a `Prepare release x.y.z` commit moves the
`UNRELEASED` entries into a version section, and the GitHub release of the tag builds and
publishes the package and the documentation.
