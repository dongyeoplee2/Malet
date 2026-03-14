# Installation

## From PyPI

```bash
pip install malet
```

## From source

```bash
pip install git+https://github.com/dongyeoplee2/Malet.git
```

## Development setup

Malet uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
git clone https://github.com/dongyeoplee2/Malet.git
cd Malet
uv sync
```

To build the documentation locally:

```bash
uv sync --group docs
uv run sphinx-build docs docs/_build/html -b html
open docs/_build/html/index.html
```

## Dependencies

The following packages are automatically installed with Malet:

| Package | Purpose |
|---------|---------|
| `absl-py` | Flag parsing and app framework |
| `gitpython` | Git metadata logging |
| `matplotlib` | Plot rendering |
| `ml-collections` | Configuration objects |
| `numpy` | Numerical operations |
| `pandas` | Experiment log DataFrames |
| `rich` | CLI output formatting |
| `seaborn` | Plot styling |
