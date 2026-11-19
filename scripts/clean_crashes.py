# clean and save to data/clean/crashes_clean.csv
# run from the main project folder: python scripts/clean_crashes.py
import pandas as pd

years = [2019, 2020, 2021, 2022, 2023, 2024]
df = pd.concat([pd.read_csv("data/raw/crashes_" + str(y) + ".csv", dtype=str) for y in years])
print("start rows:", len(df))

# 1. ensure no repeated crash ids
before = len(df)
df = df.drop_duplicates(subset="crash_record_id")
print("removed", before - len(df), "repeats")

# 2. change the raw date and make a plain date column, which is what we join on
when = pd.to_datetime(df["crash_date"], errors="coerce")
print("removed", when.isna().sum(), "rows where the date was not a real possible date")
df = df[when.notna()]
when = when[when.notna()]
df["crash_timestamp"] = when.dt.strftime("%Y-%m-%d %H:%M:%S")
df["crash_date"] = when.dt.strftime("%Y-%m-%d")

# 3. labels --> trim, make everything upper case, and change UNKNOWN to empty so it doesn't get counted like a real weather type
for col in ["weather_condition", "roadway_surface_cond", "lighting_condition", "most_severe_injury"]:
    df[col] = df[col].str.strip().str.upper()
    print(col, "-", (df[col] == "UNKNOWN").sum(), "UNKNOWN changed to empty")
    df[col] = df[col].replace("UNKNOWN", pd.NA)

# 4. speed limit: Change typo speed limits to empty
speed = pd.to_numeric(df["posted_speed_limit"], errors="coerce")
real_limit = (speed >= 5) & (speed <= 70) & (speed % 5 == 0)
print("posted_speed_limit -", (~real_limit).sum(), "values changed to empty")
df["posted_speed_limit"] = speed.where(real_limit).astype("Int64")

# 5. injury as whole numbers and where the count is missing, just leave it empty
df["injuries_total"] = pd.to_numeric(df["injuries_total"], errors="coerce").astype("Int64")
df["injuries_fatal"] = pd.to_numeric(df["injuries_fatal"], errors="coerce").astype("Int64")
print("injuries_total -", df["injuries_total"].isna().sum(), "missing values left empty")

df = df[["crash_record_id", "crash_timestamp", "crash_date", "weather_condition", "roadway_surface_cond",
         "lighting_condition", "most_severe_injury", "injuries_total", "injuries_fatal", "posted_speed_limit"]]
df = df.sort_values(["crash_timestamp", "crash_record_id"])
df.to_csv("data/clean/crashes_clean.csv", index=False)
print("saved data/clean/crashes_clean.csv with", len(df), "rows")
