# /// script
# requires-python = "==3.12.8"
# dependencies = [
#   "fastexcel==0.13.0",
#   "polars==1.27.1",
# ]
# ///

import glob
import re

import polars as pl

paths = glob.glob("./data/raw/*.xlsx")
years = [int(re.search("20[0-9]{2}", path).group()) for path in paths]
dfs = []

for path, year in zip(paths, years):
    dfs.append(
        pl.read_excel(
            path,
            read_options={
                "skip_rows": 3,
                "column_names": ["contributor", "amt", "pct"],
            },
        )
        .cast({"amt": pl.Float64})
        .with_columns(year=pl.lit(year))
    )

df = (
    pl.concat(dfs)
    .with_columns(
        contributor_fixed=pl.col("contributor")
        .str.replace_all(r"\s+", " ")
        .str.replace_all(r"\.|\,", "")
        .replace(
            {
                "PARKER MC CAY": "PARKER MCCAY",
                "PARKER MCCAY PA": "PARKER MCCAY",
                "SICKELS & ASSOCIATES INC": "SICKELS & ASSOCIATES",
                "MALEY & ASSOCIATES": "MALEY GIVENS",
                "GIVENS MALEY": "MALEY GIVENS",
                "HARDENBERGH INSURANCE GROUP INC": "HARDENBERGH INSURANCE GROUP",
                "BROWN & CONNERY LLP": "BROWN & CONNERY",
                "TAMBUSSI WILLIAM ESQ": "TAMBUSSI WILLIAM",
                "REMINGTON & VERNICK ENGINEERS INC": "REMINGTON & VERNICK",
                "REMINGTON & VERNICK ENGINEERS": "REMINGTON & VERNICK",
                "PETRONI NICK L": "PETRONI NICK",
                "ALICE JOHN A": "ALCIE JOHN",
            }
        ),
    )
    .group_by("contributor_fixed")
    .agg(pl.col("amt").sum(), year_first_contrib=pl.col("year").min())
    .sort("amt", descending=True)
)
print(df)

df.write_csv("./data/clean/summary.csv")
