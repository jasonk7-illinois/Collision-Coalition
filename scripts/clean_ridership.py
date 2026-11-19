# cleans raw cta ridership file and saves data/clean/ridership_clean.csv
# run from the main project folder: python scripts/clean_ridership.py
import pandas as pd

df = pd.read_csv("data/raw/cta_ridership_2019_2024.csv", dtype=str)
print("start rows:", len(df))

# 1. we only want the date from the raw info
day = pd.to_datetime(df["service_date"], errors="coerce")
df = df[day.notna()]
df["service_date"] = day[day.notna()].dt.strftime("%Y-%m-%d")

# 2. keep one row per day
before = len(df)
df = df.drop_duplicates(subset="service_date")
print("removed", before - len(df), "repeats")

# 3. change the day codes into words
df["day_type"] = df["day_type"].str.strip().str.upper()
df["day_type"] = df["day_type"].replace({"W": "WEEKDAY", "A": "SATURDAY", "U": "SUNDAY_HOLIDAY"})

# 4. ride total has to equal bus plus rail
df["bus_rides"] = pd.to_numeric(df["bus"], errors="coerce").astype("Int64")
df["rail_rides"] = pd.to_numeric(df["rail_boardings"], errors="coerce").astype("Int64")
df["total_rides"] = pd.to_numeric(df["total_rides"], errors="coerce").astype("Int64")
off = (df["bus_rides"] + df["rail_rides"]) != df["total_rides"]
df.loc[off, "total_rides"] = df["bus_rides"] + df["rail_rides"]
print("fixed", off.sum(), "days where the total did not equal bus + rail")

df = df[["service_date", "day_type", "bus_rides", "rail_rides", "total_rides"]].sort_values("service_date")
df.to_csv("data/clean/ridership_clean.csv", index=False)
print("saved data/clean/ridership_clean.csv with", len(df), "rows")
