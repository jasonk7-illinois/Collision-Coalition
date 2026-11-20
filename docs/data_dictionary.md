# Data Dictionary

This lists the columns in every data file our project makes. The raw files in `data/raw/` still use the original column names from each publisher and the source links are in the [README](../README.md).

## data/clean/daily_integrated.csv

This is our final combined table. It has a row for each day from January of 2019 to December of 2024 (2,192 rows) and is made by [scripts/integrate.sql](../scripts/integrate.sql).

| Column | Type | Unit | Source | Description |
|---|---|---|---|---|
| `date` | date (YYYY-MM-DD) | | all | The day. It is what all three datasets had in common, so we joined on it. |
| `day_type` | text | | CTA | Either `WEEKDAY`, `SATURDAY`, or `SUNDAY_HOLIDAY`. If a holiday is on a weekday, the CTA counts it as `SUNDAY_HOLIDAY`. |
| `crash_count` | integer | crashes | Crashes | The number of crashes reported that day. |
| `crashes_with_injury_info` | integer | crashes | Crashes | The number of crashes that day with an injury count. We use this as the bottom number when calculating percentage of crashes with injuries. |
| `injury_crash_count` | integer | crashes | Crashes | The number of crashes that day with at least one person injured. |
| `injuries_total` | integer | people | Crashes | The total number of people hurt in crashes that day, including those who died. |
| `injuries_fatal` | integer | people | Crashes | The total number of people who died in crashes that day. |
| `crashes_with_weather_info` | integer | crashes | Crashes | The number of crashes that day that had an actual weather condition written down by the officer. |
| `crashes_reported_precip` | integer | crashes | Crashes | The number of crashes that day where the officer wrote down rain, snow, freezing rain/drizzle, sleet/hail, or blowing snow. |
| `prcp_in` | decimal | inches | NOAA | How much rain/precipitation there was at O'Hare. |
| `snow_in` | decimal | inches | NOAA | How much snow there was at O'Hare. |
| `tmax_f` | decimal | °F | NOAA | Highest temperature at O'Hare that day. |
| `tmin_f` | decimal | °F | NOAA | Lowest temperature at O'Hare that day. |
| `awnd_mph` | decimal | mph | NOAA | Average wind speed at O'Hare that day. |
| `bus_rides` | integer | boardings | CTA | Number of times people got on a CTA bus. |
| `rail_rides` | integer | boardings | CTA | Number of times people got on a CTA train. |
| `total_rides` | integer | boardings | CTA | `bus_rides` and `rail_rides` added together. |
| `has_crashes` | true/false | | derived | True if the crash data had at least one row for this day. |
| `has_weather` | true/false | | derived | True if the weather data had a row for this day. |
| `has_ridership` | true/false | | derived | True if the ridership data had a row for this day. |

## data/clean/crashes_clean.csv

Each row is one crash. This file is too big for GitHub (140 mb) so it's not in the repo. However, `scripts/clean_crashes.py` rebuilds it.

| Column | Type | Description |
|---|---|---|
| `crash_record_id` | text | The crash report's unique ID. This is the primary key. |
| `crash_timestamp` | timestamp (YYYY-MM-DD HH:MM:SS) | The time the crash happened in Chicago time. |
| `crash_date` | date | The date from `crash_timestamp`. We use it to match with `weather_date` and `service_date`. |
| `weather_condition` | text | The weather the officer wrote down, like `RAIN`, or `SNOW`. Left empty if the report said unknown. |
| `roadway_surface_cond` | text | What the road was like according to the officer, like `DRY`, `WET`, or `ICE`. Left empty if unknown. |
| `lighting_condition` | text | How light or dark it was according to the officer, like `DAYLIGHT` or `DARKNESS`. Left empty if unknown. |
| `most_severe_injury` | text | The worst injury in the crash, one of: `NO INDICATION OF INJURY`, `REPORTED, NOT EVIDENT`, `NONINCAPACITATING INJURY`, `INCAPACITATING INJURY`, `FATAL`. |
| `injuries_total` | integer | Number of people hurt, including people who died. Empty if it wasn't recorded. |
| `injuries_fatal` | integer | Number of people who died. Empty if it wasn't recorded. |
| `posted_speed_limit` | integer (mph) | The speed limit where the crash happened. Left empty if the value wasn't a multiple of 5 between 5 and 70, since those aren't real speed limits. |

## data/clean/weather_clean.csv

Each row is one day.

| Column | Type | Unit | Description |
|---|---|---|---|
| `weather_date` | date | | The day the weather was measured. This is the primary key. |
| `prcp_in` | decimal | inches | How much rain/precipitation there was. |
| `snow_in` | decimal | inches | How much snow there was. |
| `tmax_f` | decimal | °F | Highest temperature. |
| `tmin_f` | decimal | °F | Lowest temperature. |
| `awnd_mph` | decimal | mph | Average wind speed. |

## data/clean/ridership_clean.csv

Each row is one day.

| Column | Type | Description |
|---|---|---|
| `service_date` | date | The day CTA was running. This is the primary key. |
| `day_type` | text | Either `WEEKDAY`, `SATURDAY`, or `SUNDAY_HOLIDAY`. |
| `bus_rides` | integer | Number of bus boardings. |
| `rail_rides` | integer | Number of train boardings. |
| `total_rides` | integer | Bus and train boardings added together. |