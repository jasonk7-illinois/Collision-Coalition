# Tim Cho — Contribution Summary, Milestone 3

Role: Acquisition & Workflow

My part this milestone was getting the repo set up and the data in.

- Set up the folders (`data/raw`, `data/clean`, `scripts`, `results`, `docs`, `contributions`), the `.gitignore` and `requirements.txt`, and described the layout and file naming in the [README](../README.md).
- Added the three acquisition scripts ([crashes](../scripts/acquire_crashes.py), [weather](../scripts/acquire_weather.py), [ridership](../scripts/acquire_ridership.py)) and the shared download and SHA-256 helper, [common.py](../scripts/common.py).
- Committed the raw data for all three sources along with [checksums.csv](../data/raw/checksums.csv), which records each file's hash, size, download time and URL.
- The crash data was too big for one file on GitHub, so it's split into one file per year and stays in the repo. No Box needed.
- Updated the timeline and the "Changes Since Milestone 2" section in [ProjectPlan.md](../ProjectPlan.md) and put together [StatusReport.md](../StatusReport.md) for the team to finish.

Next for me: the Snakemake workflow (Task 11), my share of the metadata and docs (Task 12), and the `final-project` release.
