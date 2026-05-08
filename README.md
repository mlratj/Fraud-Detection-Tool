# Fraud Detection Tool

A tool that checks whether a dataset's first-digit distribution conforms to
[Benford's Law](https://en.wikipedia.org/wiki/Benford%27s_law). Significant
deviation from the expected distribution can indicate anomalies or potential
fraud in the data.

## Requirements

- Python 3.9+
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

## Usage

```bash
uv run main.py
```

The tool will prompt you to:

1. **Choose a data source** — load a CSV from the `datasource/` directory or
   provide a URL to a remote CSV file.
2. **Select a column** — specify which numeric column to analyse.

The tool then plots a histogram comparing your data's first-digit distribution
against the theoretical Benford distribution.

If an invalid file name or column name is entered, the tool lists the available
options and prompts again.

## Running tests

```bash
uv run pytest
```
