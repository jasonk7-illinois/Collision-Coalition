# quality check of the joined table post-integration.
# check that the join worked correctly
# prints and saves results in docs/quality_post_integration.csv
# run from the main project folder: python scripts/assess_integrated.py
import pandas as pd

df = pd.read_csv("data/clean/daily_integrated.csv")
crashes = pd.read_csv("data/clean/crashes_clean.csv", usecols=["crash_record_id", "crash_date"])
weather = pd.read_csv("data/clean/weather_clean.csv")
ridership = pd.read_csv("data/clean/ridership_clean.csv")

results = []

def record(dimension, check, value):
    # adds one line to the results table
    results.append({"dimension": dimension, "check": check, "value": value})


record("size", "rows (should be one per day, 2192)", len(df))

# completeness
in_all_three = df["has_crashes"] & df["has_weather"] & df["has_ridership"]
record("completeness", "days found in crashes", df["has_crashes"].sum())
record("completeness", "days found in weather", df["has_weather"].sum())
record("completeness", "days found in ridership", df["has_ridership"].sum())
record("completeness", "days found in all", in_all_three.sum())
record("completeness", "share of days found in all", round(in_all_three.mean(), 4))
record("completeness", "dates missing from at least one source", " | ".join(df.loc[~in_all_three, "date"]))
for col in df.columns:
    record("completeness", col + " part filled in", round(df[col].notna().mean(), 4))

# consistency --> the join should not change, lose, or repeat things
record("consistency", "repeats", df["date"].duplicated().sum())
record("consistency", "crashes added up", int(df["crash_count"].sum()))
record("consistency", "rows in crashes_clean.csv", len(crashes))
record("consistency", "days where total does not equal bus + rail", ((df["bus_rides"] + df["rail_rides"]) != df["total_rides"]).sum())
record("consistency", "days with more injury crashes than crashes", (df["injury_crash_count"] > df["crash_count"]).sum())
record("consistency", "days with more deaths than injuries", (df["injuries_fatal"] > df["injuries_total"]).sum())
record("consistency", "days where low temp is greater than the high", (df["tmin_f"] > df["tmax_f"]).sum())

# timeliness
record("timeliness", "crashes first and last date", crashes["crash_date"].min() + " to " + crashes["crash_date"].max())
record("timeliness", "weather first and last date", weather["weather_date"].min() + " to " + weather["weather_date"].max())
record("timeliness", "ridership first and last date", ridership["service_date"].min() + " to " + ridership["service_date"].max())
record("timeliness", "joined table first and last date", df["date"].min() + " to " + df["date"].max())

# accuracy --> does reported weather match the noaa that day?
# for each day, what share of crash reports said rain or snow
precip = df["crashes_reported_precip"] / df["crashes_with_weather_info"]
dry = (df["prcp_in"] == 0) & (df["snow_in"].fillna(0) == 0)
wet = (df["prcp_in"] >= 0.1) | (df["snow_in"] >= 0.1)
record("accuracy", "noaa dry days", dry.sum())
record("accuracy", "noaa wet days (>= 0.1 inch)", wet.sum())
# if the reports are accurate the dry number should be near 0 and the wet number a lot higher
record("accuracy", "avg share of reports saying rain/snow on dry days", round(precip[dry].mean(), 4))
record("accuracy", "avg share of reports saying rain/snow on wet days", round(precip[wet].mean(), 4))
record("accuracy", "correlation between noaa rain and share of reports saying rain/snow", round(df["prcp_in"].corr(precip), 3))

report = pd.DataFrame(results)
report.to_csv("docs/quality_post_integration.csv", index=False)
print(report.to_string(index=False))
print("saved docs/quality_post_integration.csv")
