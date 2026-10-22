# Project Plan: Weather, Transit Ridership, and Daily Traffic Crashes in Chicago

Team: Collision Coalition — Jason Kim, Joseph Choi, Saif Farooq, Tim Cho

Repository: [https://github.com/jasonk7-illinois/Collision-Coalition](https://github.com/jasonk7-illinois/Collision-Coalition) 

## Overview

Our goal is to find out whether daily weather and daily public-transit ridership are related to how many traffic crashes happen in Chicago each day, and how serious those crashes are. To do this we will acquire, assess, clean, and integrate three public datasets that all share a date as a common key (City of Chicago's traffic crash records, NOAA's daily weather observations for Chicago, and the CTA's daily ridership totals).

The project follows the data curation workflow taught in this course. We will (1) acquire each dataset with Python scripts and verify the downloaded files with SHA-256 hashes, (2) store the raw files as CSV and load them into a DuckDB database defined by a `schema.sql` file, (3) assess the quality of each dataset on accuracy, completeness, timeliness, and consistency, (4) clean the problems we find with scripts (or OpenRefine, with the exported operation history), (5) integrate the cleaned datasets by aggregating crashes to one row per day and joining to weather and ridership on the date, (6) assess the quality of the integrated table, and (7) run a simple analysis with at least one visualization. All steps will be separate scripts run in order by a run-all script or Snakemake workflow so that a grader can reproduce our results from a fresh clone of the repository.

## Roles

- Tim Cho (Acquisition & Workflow)
    - Write the acquisition scripts (Python `requests` + SHA-256 checks), set up the repository folder structure and `requirements.txt`, build the run-all / Snakemake workflow, create the GitHub tags and releases.
- Jason Kim (Storage & Integration)
    - Write `schema.sql` and the DuckDB load script, draw the ER diagram, write the integration script that aggregates crashes by day and joins the three tables on date.
- Joseph Choi (Data Quality & Cleaning)
    - Profile each dataset, write the pre- and post-integration quality assessments (four dimensions), write the cleaning scripts and document what each one fixes.
- Saif Farooq (Analysis & Documentation) 
    - Write the analysis and visualization script, keep the data dictionary and README up to date, handle licenses, citations, and the metadata file.

## Research Questions

1. Weather: Do days with rain, snow, or freezing temperatures have more crashes, and a higher share of injury crashes, than dry, mild days?
2. Ridership: On days when more people ride the CTA, are there fewer crashes? Does this pattern hold separately for weekdays and weekends?
3. Reporting accuracy: How often does the `WEATHER_CONDITION` that an officer records in a crash report agree with the weather NOAA actually observed that day? (This also serves as part of our accuracy assessment.)

All three questions can be answered from the integrated daily table described below.

## Datasets

All three sources come from portals on the instructor's dataset list (City of Chicago Data Portal and U.S. government open data). None are from Kaggle.

### 1. Traffic Crashes – Crashes (City of Chicago Data Portal)

- **URL:** [https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if](https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if)
- **Format / access:** CSV download via the portal's API with `requests`.
- **Size:** Over 900,000 crash records since 2015, updated daily. We plan to use 2019–2024.
- **Fields we will use:** `CRASH_RECORD_ID`, `CRASH_DATE`, `WEATHER_CONDITION`, `ROADWAY_SURFACE_COND`, `LIGHTING_CONDITION`, `MOST_SEVERE_INJURY`, `INJURIES_TOTAL`, `INJURIES_FATAL`, `POSTED_SPEED_LIMIT`.
- **Link key:** the date part of `CRASH_DATE`.
- **Terms of use:** City of Chicago open data terms; free to reuse with attribution. The Crashes table contains no personal information (we will not use the companion People table).

### 2. Daily Weather Summaries, Chicago O'Hare (NOAA NCEI)

- **URL:** [https://www.ncei.noaa.gov/access/services/data/v1](https://www.ncei.noaa.gov/access/services/data/v1) (station `USW00094846`, dataset `daily-summaries`)
- **Format / access:** CSV via the NCEI data service API.
- **Size:** One row per day; about 2,200 rows for 2019–2024.
- **Fields:** `DATE`, `PRCP` (precipitation), `SNOW`, `TMAX`, `TMIN`, `AWND` (wind).
- **Link key:** `DATE`.
- **Terms of use:** U.S. government work, public domain; NCEI asks to be cited.

### 3. CTA Ridership – Daily Boarding Totals (City of Chicago Data Portal)

- **URL:** [https://data.cityofchicago.org/Transportation/CTA-Ridership-Daily-Boarding-Totals/6iiy-9s97](https://data.cityofchicago.org/Transportation/CTA-Ridership-Daily-Boarding-Totals/6iiy-9s97)
- **Format / access:** CSV via the portal's API.
- **Size:** One row per day since 2001; about 2,200 rows for 2019–2024.
- **Fields:** `service_date`, `day_type` (weekday / Saturday / Sunday-holiday), `bus`, `rail_boardings`, `total_rides`.
- **Link key:** `service_date`.
- **Terms of use:** City of Chicago open data terms.

**Why these can be integrated:** every dataset has exactly one date per row (after we aggregate crashes to daily counts), so the join is a straightforward relational join on a date column. Each source contributes different information: crashes are the outcome, weather and ridership are daily conditions. The integrated table will have one row per day with crash counts, injury counts, weather measurements, and ridership totals. We expect the main integration challenges to be schema-level (different date formats, column names, and units across the three sources), which is exactly what Modules 7–8 cover.

## Timeline

Milestone 2 (this plan) is due **Oct 22**. Canvas has not yet posted the Milestone 3 and 4 due dates, so later dates below are our own targets and will be updated when the official dates appear.

|  | Task | What it involves | Course module | Owner | Target |
| --- | --- | --- | --- | --- | --- |
| 1 | Repository setup | Folder layout (`data/raw`, `data/clean`, `scripts`, `results`, `docs`), `.gitignore`, `requirements.txt`, a short file-naming convention in the README | 2 | Tim | Oct 26 |
| 2 | Acquisition scripts | One script per dataset using `requests`; save CSVs to `data/raw`; compute and record SHA-256 for each file; record the download date | 4 | Tim | Oct 30 |
| 3 | Legal / ethical check | Write up the terms of use for each source and confirm no personal data is used | 3 | Saif | Oct 30 |
| 4 | Storage model | `schema.sql` with three tables and primary keys; DuckDB load script using `COPY`; ER diagram (draw.io) | 5–6 | Jason | Nov 3 |
| 5 | Pre-integration quality assessment | For each dataset, measure the four dimensions from Week 9: accuracy (syntactic: do dates, numbers, and category labels match the expected format/range; semantic: spot-check values against an outside source), completeness (column completeness = non-null ÷ total for each field; temporal completeness = are any days missing), timeliness (when was each source last updated, and how often does it change), consistency (rule checks such as `INJURIES_FATAL ≤ INJURIES_TOTAL`, `TMIN ≤` `TMAX`, `bus + rail = total_rides`, no duplicate crash IDs); write results to `docs/` | 9–10 | Joseph | Nov 7 |
| 6 | Cleaning scripts | Fix the specific issues found in Task 5 (parse dates to one format, standardize category labels, handle missing days, remove duplicates); document each fix | 11–12 | Joseph | Nov 11 |
| 7 | Integration script | Aggregate crashes to one row per day; join to weather and ridership on date; save integrated CSV and load to DuckDB | 7–8 | Jason | Nov 14 |
| 8 | Post-integration quality assessment | Repeat the four dimensions on the integrated table: completeness = share of days with a match in all three sources and a list of unmatched dates; consistency = one row per date, totals still add up; timeliness = all sources cover the same date range; accuracy = compare the officer-reported `WEATHER_CONDITION` to NOAA's observed precipitation for the same day (semantic accuracy checked against an independent source, as in Week 9) | 10 | Joseph | Nov 17 |
| 9 | **Milestone 3: Status report** | `StatusReport.md`, updated plan, each member's contribution note, `status-report` release | — | All | TBD Canvas |
| 10 | Analysis & visualization | Compare daily crash counts and injury rates across weather and ridership conditions; produce at least one chart; save results to `results/` | — | Saif | Nov 25 |
| 11 | Workflow automation | Run-all script or Snakefile that runs Tasks 2, 4–8, 10 in order; test on a fresh clone | 13 | Tim | Dec 2 |
| 12 | Metadata & documentation | Data dictionary (text file), machine-readable metadata file (format per Module 15), LICENSE files for code and data, `pip freeze` output | 14–15 | Saif, Tim | Dec 5 |
| 13 | Final README | All required report sections with links to the repository files; "Reproducing" steps; references | 14 | All | Dec 9 |
| 14 | **Milestone 4: Final release** | Fresh-clone test, `final-project` release, submit on Canvas | — | All | TBD Canvas |

**Data lifecycle:** We will relate our steps to the data science lifecycle introduced in Module 1 (plan → acquire → process/clean → integrate → analyze → preserve/share), and point out in the final report where each script fits.

## Constraints

- **File size.** The full crash CSV is well over GitHub's 50 MB limit. We will download only the years and columns we need; if the file is still too large we will store it on Illinois Box with a download step in the workflow and a shareable link in the README.
- **The crash data changes daily.** Re-downloading later will give different counts. We will record the download date and SHA-256 of the file we used, and the workflow will use the saved copy.
- **One weather station.** O'Hare is at the far northwest edge of the city, so weather elsewhere in Chicago may differ. We may add the Midway station as a second check.
- **Reported crashes only.** Minor crashes often go unreported, so our counts describe reported crashes.
- **Holidays and COVID.** Ridership dropped sharply in 2020–2021 and holidays have unusual patterns. We will use the `day_type` field and note these periods in the analysis.
- **Aggregation.** Joining on date means we lose crash-level detail such as location. Our questions are about daily patterns, so this is acceptable, but it limits what we can say.

## Gaps

- **Milestone 3 and 4 due dates** are not yet on Canvas; the timeline will be updated when they appear.
- **Modules 13–15** (workflow automation, reproducibility, metadata) have not been taught yet. We know a Snakefile or run-all script and a machine-readable metadata file are required but will finalize tool choices after those modules.
- **OpenRefine vs. scripts for cleaning.** OpenRefine is introduced in next week's lab; we will decide afterward whether to use it (with its exported operation history) or pandas scripts for cleaning.
- **Instructor feedback** on whether the officer-reported vs. NOAA weather agreement check is a good accuracy test, and whether our three sources are considered sufficiently distinct.
- **Possible extension.** If time allows, we could add neighborhood-level data (e.g., Census ACS) as a fourth source, but that would require mapping crash coordinates to geographic areas, which we have not covered in class and would only attempt after the core pipeline works.
