# Contractor contributions

This project compiles data on political contributions made to candidates for elected office in Glassboro, NJ.

## Data

All data come from the NJ Election Law Enforcement Commission's (ELEC) Candidate and Committee Reports [database](https://www.njelecefilesearch.com/searchcandidatereports).

This project creates a summary data file, [`data/clean/summary.csv`](./data/clean/summary.csv), containing total contributions made to all candidates of any party in all general elections (no primaries) from 2015 to 2024, aggregated by contributor.

## Usage

To recreate the data files, first install [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

Then run in this directory:

```sh
uv run main.py
```
