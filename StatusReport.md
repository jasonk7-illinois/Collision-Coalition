# Status Report: Weather, Transit Ridership, and Daily Traffic Crashes in Chicago

Team: Collision Coalition — Jason Kim, Joseph Choi, Saif Farooq, Tim Cho

Milestone 3, November 19, 2026

## Summary

Our project plan has been slightly altered as we've fallen a bit behind schedule. When the project plan was marked, Tasks 1–8 were scheduled for completion between October 26 and November 17, and none had been uploaded to the repository by the start of the week. Now, as I write, the repository structure and the data acquisition step (Tasks 1 and 2) are finished and the raw data for all three sources is in the repository, which clears the way for all subsequent tasks. New target dates for storage, quality assessment, cleaning and integration (Tasks 3–8) are given below. The project scope, datasets and research questions remain the same.

## Task Updates

Task numbers match the timeline in [ProjectPlan.md](ProjectPlan.md).

### Task 1: Repository setup (Tim) — Done

The repository now reflects the planned folder structure: [`data/raw`](data/raw), [`data/clean`](data/clean), [`scripts`](scripts), [`results`](results) and [`docs`](docs). We have added a [`contributions`](contributions) folder for each student to submit their summary. In the root, we have added [.gitignore](.gitignore) and [requirements.txt](requirements.txt) files. The [README](README.md) is now updated with the folder structure and information regarding how files are named.

### Task 2: Acquisition scripts (Tim) — Done

There is one acquisition script per source, all using Python `requests`:

- [scripts/acquire_crashes.py](scripts/acquire_crashes.py) downloads the nine crash columns named in our plan from the City of Chicago Data Portal API, one CSV per year for 2019–2024 ([data/raw/crashes_2019.csv](data/raw/crashes_2019.csv) through [crashes_2024.csv](data/raw/crashes_2024.csv)). In total this is about 650,000 crash records, between roughly 92,000 and 118,000 per year.
- [scripts/acquire_weather.py](scripts/acquire_weather.py) downloads NOAA daily summaries (PRCP, SNOW, TMAX, TMIN, AWND) for the Chicago O'Hare station into [data/raw/weather_ohare_2019_2024.csv](data/raw/weather_ohare_2019_2024.csv).
- [scripts/acquire_ridership.py](scripts/acquire_ridership.py) downloads CTA daily boarding totals into [data/raw/cta_ridership_2019_2024.csv](data/raw/cta_ridership_2019_2024.csv), 2,192 rows, one for every day from January 1, 2019 to December 31, 2024.

All three scripts share a common utility script ([scripts/common.py](scripts/common.py)), which is responsible for performing the download and ensuring its integrity. As none of our sources provide a hash, the script computes the SHA-256 for each downloaded file and stores it (along with the file size, download timestamp, and the exact request URL used) in [data/raw/checksums.csv](data/raw/checksums.csv). On any subsequent run, it does not re-download the file. Instead, it computes the hash of the local file and aborts with an error if it does not match what was originally recorded.

### Task 3: Legal / ethical check (Saif) — Not started

> TODO (Saif): confirm or correct this status and add a link if anything exists.

The terms of use for each source were identified in the project plan (City of Chicago open data terms for crashes and ridership; public domain for NOAA). The written check and the license files are still to do.

### Task 4: Storage model (Jason) — In Progress

[schema.sql](scripts/schema.sql) and [load_db.py](scripts/load_db.py) have both been committed. The first load and ER diagram still need to be done, and the load can not be done without the cleaned files from task 6.

### Tasks 5, 6, and 8: Quality assessment and cleaning (Joseph) — In progress

The five scripts have been committed but not yet run, with a link to each. The results and cleaned files follow the timeline dates. A first look at the raw crash files already shows something for the assessment to measure: `weather_condition`, `roadway_surface_cond`, and `lighting_condition` contain the value `UNKNOWN`, which will count against completeness even though the cells are not empty.

### Task 7: Integration script (Jason) — In Progress

[Integrate.sql](scripts/integrate.sql) and [integrate.py](scripts/integrate.py) have both been committed. They have not been run yet since they need the cleaned data from task 6.

### Tasks 10–14: Analysis, workflow, metadata, README, final release — Not started

These were always scheduled after this milestone. The acquisition scripts were written so that a run-all script or Snakefile can call them as the first stage of the workflow without changes.

## Updated Timeline

| # | Task | Owner | Original target | Status | New target |
|---|---|---|---|---|---|
| 1 | Repository setup | Tim | Oct 26 | Done | Nov 19 |
| 2 | Acquisition scripts | Tim | Oct 30 | Done | Nov 19 |
| 3 | Legal / ethical check | Saif | Oct 30 | Not started | Nov 23 |
| 4 | Storage model (`schema.sql`, DuckDB load, ER diagram) | Jason | Nov 3 | In Progress | Nov 24 |
| 5 | Pre-integration quality assessment | Joseph | Nov 7 | In progress | Nov 27 |
| 6 | Cleaning scripts | Joseph | Nov 11 | In progress | Dec 1 |
| 7 | Integration script | Jason | Nov 14 | In Progress | Dec 3 |
| 8 | Post-integration quality assessment | Joseph | Nov 17 | In progress | Dec 5 |
| 9 | Milestone 3: status report | All | TBD | Done | Nov 19 |
| 10 | Analysis and visualization | Saif | Nov 25 | Not started | Dec 7 |
| 11 | Workflow automation | Tim | Dec 2 | Not started | Dec 8 |
| 12 | Metadata and documentation | Saif, Tim | Dec 5 | Not started | Dec 8 |
| 13 | Final README | All | Dec 9 | Not started | Dec 9 |
| 14 | Milestone 4: final release | All | TBD | Not started | TBD (not yet on Canvas) |

Tasks 3, 4, and 5 do not depend on each other, so they will run in parallel over fall break. The order quality assessment, then cleaning, then integration, then analysis is kept. If Canvas posts a Milestone 4 date earlier than December 9, we will shorten Tasks 10–13.

## Changes to the Project Plan

[ProjectPlan.md](ProjectPlan.md) has been updated. The changes are listed in its new "Changes Since Milestone 2" section:

- **Feedback from Milestone 2.** The grader pointed out that research question 3, how often the officer-reported `WEATHER_CONDITION` agrees with NOAA's observations, is more of a data-quality check than a research question. We agree and have kept it, but it is now reported mainly as the accuracy dimension of the post-integration quality assessment (Task 8). Questions 1 and 2 are the main analysis questions.
- **Timeline.** All target dates were revised as shown above.
- **Crash data storage.** The plan said we would put the crash file on Illinois Box if it was too large for GitHub. We now download one file per year instead, so all input data is in the repository and no Box download step is needed.
- **Checksums.** The plan said we would "compute and record SHA-256 for each file". We made this specific: hashes are recorded at first download and verified on every run.

Two items from the Gaps section of the plan are still open: whether cleaning will use OpenRefine or pandas scripts, and whether the workflow will be a run-all script or Snakemake. Both will be decided when those tasks start.

## Challenges

**The schedule has been slightly altered.** The original plan had eight tasks following Milestone 2, spaced over four weeks. All of them depended on the completion of the previous one. Tasks 1 and 2 were not finished as scheduled, so no subsequent tasks could start on time. *Plan:* now, with the raw data finally in the repository, the dependency issue is out of the way. We can now carry out Tasks 3, 4 and 5 at the same time, and will check progress as a team on each new target date.

**The crash data is simply too big to be one file.** With just nine columns it is still 146 MB for the years 2019–2024, since the `CRASH_RECORD_ID` field contains 128-character strings, exceeding GitHub's 50 MB limit. *Resolved:* the acquisition script fetches only one year at a time. Each yearly file is 21–26 MB.

**The API only provides 1,000 rows by default.** Unless a limit is specified, the Chicago Data Portal API cuts off the results at 1,000 rows without any warning. *Resolved:* each request sets a `$limit` well above the size of the largest year, along with an `$order`, so the same data always results in the same file and, in turn, the same hash.

**The crash records are dynamic and the sources do not supply hashes.** Re-downloading can result in a different file, which would violate reproducibility. *Resolved:* the committed files are the copy of record. The script verifies each saved file against its hash, but does not overwrite it. [checksums.csv](data/raw/checksums.csv) keeps track of each file's hash and the time of download.

**Commit history.** Until this point, no commits other than project plan uploads from two members via a web browser had been made. *Plan:* from here on, everyone on the team will commit their work to the GitHub repository using their own account. This change begins with the contribution summaries presented below.

## Individual Contributions

Each member wrote and committed their own summary:

- [Tim Cho](contributions/tim-cho.md)
- [Jason Kim](contributions/jason-kim.md)
- [Joseph Choi](contributions/joseph-choi.md)
- [Saif Farooq](contributions/saif-farooq.md)
