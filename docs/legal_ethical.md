# Legal and Ethical Check

This file explains whether we're allowed to use our three datasets, what the terms require us to do, and all the ethical concerns we need to think about. We checked the terms pages on Nov 19, 2026.

## Terms of use

### Traffic Crashes – Crashes (City of Chicago)
- Terms: [Data Portal terms of use](https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html)
- We are allowed to use, show, and share the data. However, the City says it can have anyone stop using it at any given time.
- The City gives the data just how it is and doesn't assure it's up to date or complete or even accurate and it is all subject to change.
- Anything we make with the data from the dataset has to include the City's disclaimer which basically says the data was modified from its original source (www.cityofchicago.org). We have to say that the City doesn't vouch for the accuracy of the data and it can change at any time. We'll add this into our final README.
- If someone makes a claim because of how we used the data, that is our responsibility, not the City's (the indemnity part of the terms).
- We also have to follow any extra rules from the department that owns the data.

### CTA Ridership – Daily Boarding Totals (Chicago Transit Authority, via the City of Chicago Data Portal)
- Terms: [Data Portal terms of use](https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html)
- The dataset page lists the license as "See Terms of Use," so the same rules apply as the dataset above.
- The CTA doesn't list any extra terms for this dataset.

### Daily Summaries (GHCN-Daily), station USW00094846 (NOAA NCEI)
- This is U.S. government data, so it isn't copyrighted in the US and we are allowed to use and share it freely.
- The only thing we have to do is cite NOAA NCEI as the source.

## Personal information
- We are only using the main Crashes table. We skipped the People and Vehicles tables because those have info about drivers, passengers, and cars.
- The nine crash columns we keep don't have names, addresses, plates, or locations. `scripts/acquire_crashes.py` only downloads those nine columns, so nothing else gets into the repo.
- `CRASH_RECORD_ID` is just a report number that the City makes and it doesn't lead to a person.
- The weather and ridership data are daily totals with nothing about individual people.

## Ethical considerations
- These crashes are real events where people got hurt or died, so we only look at the daily totals and never call out a single crash.
- The data only has crashes that got reported, so a lot of our crash numbers are lower than the actual because a lot of small crashes never get reported.
- `WEATHER_CONDITION` is what the officer wrote down at the scene. We compare it to NOAA as an accuracy check, but if they don't match it doesn't mean the officer messed up.

## Licenses in this repo
- Our code uses the MIT License, see [LICENSE](../LICENSE).
- The data in `data/raw/` and `data/clean/` still falls under each publisher's terms listed above. We don't claim we own any of it.
