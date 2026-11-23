# Scientific Calculator

Desktop scientific calculator with function graphing, built to grow: new maths domains
(complex numbers, matrices, equations, and later Fourier/Laplace transforms or an online
version) plug into a UI-free engine. The first version targets the features of the Casio
fx-991SP CW as a checklist, plus function graphs.

The project is at the scaffolding stage: the app opens an empty window.

## Setup

Requires Python 3.14.

```bash
python3.14 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt -e .
.venv/bin/pre-commit install
```

On Linux, Qt needs the usual desktop libraries (for example `libegl1`, `libxkbcommon0`,
`libgl1`, `libdbus-1-3` and `libxcb-cursor0`).

## Running

```bash
.venv/bin/python -m scientific_calculator
```

`--smoke` starts the app, shows the window and quits with exit code 0. CI uses it as a
headless launch check (with `QT_QPA_PLATFORM=offscreen`).

### Logging

Set `SCIENTIFIC_CALCULATOR_LOG_LEVEL` to `DEBUG`, `INFO` (default), `WARNING` or `ERROR`.
Logs go to stderr; packaged builds without a console write to a rotating `app.log` in:

- Linux: `$XDG_STATE_HOME/scientific-calculator` (default `~/.local/state/scientific-calculator`)
- Windows: `%LOCALAPPDATA%\scientific-calculator\logs`
- macOS: `~/Library/Logs/scientific-calculator`

## Project layout

- `src/scientific_calculator/engine/`: calculations, one module per maths domain, no UI imports.
- `src/scientific_calculator/ui/`: PySide6 (Qt 6) interface.
- `docs/uml.md` and `docs/flows.md`: architecture and flow diagrams.

## Checks

Both must pass before every push:

```bash
.venv/bin/pytest --cov
.venv/bin/pre-commit run --all-files
```

CI (`.github/workflows/check-code.yml`) runs pre-commit, the tests with coverage, and the
SonarCloud analysis with its quality gate on every pull request and every push to `master`.

## Branching and releases

- Work on feature branches from `develop`; squash-merge them into `develop` with a
  [Conventional Commits](https://www.conventionalcommits.org) subject (`feat:`, `fix:`, ...).
- Merge `develop` into `master` with a merge commit. When the checks pass on `master`,
  python-semantic-release bumps the version, updates `CHANGELOG.md`, tags `vX.Y.Z` and creates
  the GitHub Release. `feat` gives a minor bump and `fix`/`perf` a patch bump; other types
  do not release.
- Each release carries desktop builds: Linux x86_64 (`.tar.gz`), Windows x86_64 and macOS
  Apple Silicon (`.zip`).

### First launch of the downloaded builds

The builds are not code-signed, so the OS warns on first launch:

- Windows: on the SmartScreen prompt, choose "More info", then "Run anyway".
- macOS: open the app once, then go to System Settings → Privacy & Security and choose
  "Open Anyway". Alternatively run `xattr -dr com.apple.quarantine "Scientific Calculator.app"`.
- Linux: extract the archive and run `scientific-calculator/scientific-calculator`.

## License

MIT
