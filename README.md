# Weather, Transit Ridership, and Daily Traffic Crashes in Chicago

IS 477 course project (Fall 2026) by team Collision Coalition: Jason Kim, Joseph Choi, Saif Farooq, Tim Cho.

This README is a work in progress and will become the final project report (Milestone 4). For now see:

- [ProjectPlan.md](ProjectPlan.md) for the project plan (updated for Milestone 3)
- [StatusReport.md](StatusReport.md) for the interim status report

## Repository layout

| Path | What goes there |
|---|---|
| `data/raw/` | Files exactly as downloaded, plus `checksums.csv` (SHA-256, size, download time, and source URL of each file). Never edited by hand. |
| `data/clean/` | Cleaned and integrated files produced by scripts. |
| `scripts/` | One single-purpose script per workflow step. |
| `results/` | Analysis outputs and figures. |
| `docs/` | Quality assessment write-ups, ER diagram, data dictionary. |
| `contributions/` | One contribution summary per team member, per milestone. |

## Naming conventions

- Lowercase, words separated by underscores, no spaces.
- Scripts start with the step they perform: `acquire_`, `load_`, `assess_`, `clean_`, `integrate_`, `analyze_`.
- Data files are named `<source>_<coverage>.csv`, for example `crashes_2019.csv` or `weather_ohare_2019_2024.csv`.

## Getting the data

Run everything from the main project folder.

```bash
pip install -r requirements.txt
python scripts/acquire_crashes.py
python scripts/acquire_weather.py
python scripts/acquire_ridership.py
```

Each script downloads its source into `data/raw/` with `requests`. If a file is already there, the script does not download it again; it recomputes the file's SHA-256 and compares it with the value recorded in `data/raw/checksums.csv`, and stops with an error if they differ. The raw files are committed to this repository, so on a fresh clone the scripts only verify them.

| Dataset | Source | Files |
|---|---|---|
| Traffic Crashes – Crashes | [City of Chicago Data Portal](https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if) | `data/raw/crashes_2019.csv` … `crashes_2024.csv` |
| Daily Summaries, Chicago O'Hare (USW00094846) | [NOAA NCEI](https://www.ncei.noaa.gov/access/services/data/v1) | `data/raw/weather_ohare_2019_2024.csv` |
| CTA Ridership – Daily Boarding Totals | [City of Chicago Data Portal](https://data.cityofchicago.org/Transportation/CTA-Ridership-Daily-Boarding-Totals/6iiy-9s97) | `data/raw/cta_ridership_2019_2024.csv` |
