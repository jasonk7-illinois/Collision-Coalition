# quality check of the raw datasets before cleaning
# looks at accuracy, completeness, timeliness, consistency
# saved in docs/quality_pre_integration.csv
# run from the main project folder: python scripts/assess_raw.py
import pandas as pd

TOTAL_DAYS = 2192  # days from 2019-01-01 to 2024-12-31

results = []

def record(dataset, dimension, check, value):
    # adds one line to the results table
    results.append({"dataset": dataset, "dimension": dimension, "check": check, "value": value})


years = [2019, 2020, 2021, 2022, 2023, 2024]
crashes = pd.concat([pd.read_csv("data/raw/crashes_" + str(y) + ".csv", dtype=str) for y in years])
weather = pd.read_csv("data/raw/weather_ohare_2019_2024.csv", dtype=str)
ridership = pd.read_csv("data/raw/cta_ridership_2019_2024.csv", dtype=str)
checksums = pd.read_csv("data/raw/checksums.csv")

# crashes
dates = pd.to_datetime(crashes["crash_date"], errors="coerce")
speed = pd.to_numeric(crashes["posted_speed_limit"], errors="coerce")
injuries = pd.to_numeric(crashes["injuries_total"], errors="coerce")
fatal = pd.to_numeric(crashes["injuries_fatal"], errors="coerce")

record("crashes", "size", "rows", len(crashes))

# accuracy: are the values in the format and range they should be
record("crashes", "accuracy", "crash_date that is not a real date", dates.isna().sum())
record("crashes", "accuracy", "crash_date outside range", ((dates.dt.year < 2019) | (dates.dt.year > 2024)).sum())

# checking real speed limits
real_limit = (speed >= 5) & (speed <= 70) & (speed % 5 == 0)
record("crashes", "accuracy", "posted_speed_limit that is not real", (~real_limit).sum())
record("crashes", "accuracy", "injuries_total below zero", (injuries < 0).sum())
for col in ["weather_condition", "roadway_surface_cond", "lighting_condition", "most_severe_injury"]:
    record("crashes", "accuracy", "labels used in " + col, " | ".join(sorted(crashes[col].dropna().unique())))

# completeness
for col in crashes.columns:
    record("crashes", "completeness", col + " part filled in", round(crashes[col].notna().mean(), 4))

# Unknowns
for col in ["weather_condition", "roadway_surface_cond", "lighting_condition"]:
    record("crashes", "completeness", col + " part UNKNOWN", round((crashes[col] == "UNKNOWN").mean(), 4))
record("crashes", "completeness", "days with no crashes", TOTAL_DAYS - dates.dt.date.nunique())

#timeliness
record("crashes", "timeliness", "downloaded at", checksums.loc[checksums["file"] == "crashes_2024.csv", "downloaded_at"].iloc[0])
record("crashes", "timeliness", "most recent crash", dates.max())

# consistency
record("crashes", "consistency", "repeated crash_record_id", crashes["crash_record_id"].duplicated().sum())
record("crashes", "consistency", "more deaths than total injuries", (fatal > injuries).sum())
record("crashes", "consistency", "FATAL label not matching injuries_fatal", ((crashes["most_severe_injury"] == "FATAL") != (fatal > 0)).sum())

# weather (trim before checking)
weather.columns = weather.columns.str.strip()
for col in weather.columns:
    weather[col] = weather[col].str.strip()
weather = weather.replace("", pd.NA)

w_dates = pd.to_datetime(weather["DATE"], errors="coerce")
prcp = pd.to_numeric(weather["PRCP"], errors="coerce")
snow = pd.to_numeric(weather["SNOW"], errors="coerce")
tmax = pd.to_numeric(weather["TMAX"], errors="coerce")
tmin = pd.to_numeric(weather["TMIN"], errors="coerce")

record("weather", "size", "rows", len(weather))

record("weather", "accuracy", "DATE that is not real", w_dates.isna().sum())
record("weather", "accuracy", "PRCP <0 or >10 inches", ((prcp < 0) | (prcp > 10)).sum())
record("weather", "accuracy", "SNOW <0 or >30 inches", ((snow < 0) | (snow > 30)).sum())
record("weather", "accuracy", "TMAX <-30 or >110 F", ((tmax < -30) | (tmax > 110)).sum())
record("weather", "accuracy", "TMIN <-30 or >110 F", ((tmin < -30) | (tmin > 110)).sum())
record("weather", "accuracy", "lowest and highest TMAX", str(tmax.min()) + " to " + str(tmax.max()))
record("weather", "accuracy", "lowest and highest TMIN", str(tmin.min()) + " to " + str(tmin.max()))

for col in weather.columns:
    record("weather", "completeness", col + " part filled in", round(weather[col].notna().mean(), 4))
record("weather", "completeness", "days missing from the file", TOTAL_DAYS - w_dates.nunique())

record("weather", "timeliness", "downloaded at", checksums.loc[checksums["file"] == "weather_ohare_2019_2024.csv", "downloaded_at"].iloc[0])
record("weather", "timeliness", "first and last date", str(w_dates.min().date()) + " to " + str(w_dates.max().date()))

record("weather", "consistency", "repeated DATE", weather["DATE"].duplicated().sum())
record("weather", "consistency", "low temp above high temp", (tmin > tmax).sum())
record("weather", "consistency", "rows from some other station", (weather["STATION"] != "USW00094846").sum())

# ---------------- ridership ----------------
r_dates = pd.to_datetime(ridership["service_date"], errors="coerce")
bus = pd.to_numeric(ridership["bus"], errors="coerce")
rail = pd.to_numeric(ridership["rail_boardings"], errors="coerce")
total = pd.to_numeric(ridership["total_rides"], errors="coerce")

record("ridership", "size", "rows", len(ridership))

record("ridership", "accuracy", "service_date that is not a real date", r_dates.isna().sum())
record("ridership", "accuracy", "day_type that is not W, A or U", (~ridership["day_type"].isin(["W", "A", "U"])).sum())
record("ridership", "accuracy", "ride counts that are zero or below", ((bus <= 0) | (rail <= 0) | (total <= 0)).sum())
record("ridership", "accuracy", "weekdays marked U (holidays)", ((r_dates.dt.dayofweek < 5) & (ridership["day_type"] == "U")).sum())
# W = weekday
# A = saturday
# U = sunday or holiday (mon-fri marked U should be a holiday)

for col in ridership.columns:
    record("ridership", "completeness", col + " part filled in", round(ridership[col].notna().mean(), 4))
record("ridership", "completeness", "days missing from the file", TOTAL_DAYS - r_dates.nunique())

record("ridership", "timeliness", "downloaded at", checksums.loc[checksums["file"] == "cta_ridership_2019_2024.csv", "downloaded_at"].iloc[0])
record("ridership", "timeliness", "first and last date", str(r_dates.min().date()) + " to " + str(r_dates.max().date()))

record("ridership", "consistency", "repeated service_date", ridership["service_date"].duplicated().sum())
record("ridership", "consistency", "bus + rail does not equal total", ((bus + rail) != total).sum())

report = pd.DataFrame(results)
report.to_csv("docs/quality_pre_integration.csv", index=False)
print(report.to_string(index=False))
print("saved docs/quality_pre_integration.csv")
