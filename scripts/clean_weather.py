# cleans the raw weather file and saves to data/clean/weather_clean.csv
import pandas as pd

df = pd.read_csv("data/raw/weather_ohare_2019_2024.csv", dtype=str)
print("start rows:", len(df))

# 1. strip spaces and clean blanks
df.columns = df.columns.str.strip()
for col in df.columns:
    df[col] = df[col].str.strip()
df = df.replace("", pd.NA)

# 2. make the date (YYYY-MM-DD), drop dates that aren't real, keep one row per day
day = pd.to_datetime(df["DATE"], errors="coerce")
df = df[day.notna()]
df["weather_date"] = day[day.notna()].dt.strftime("%Y-%m-%d")
before = len(df)
df = df.drop_duplicates(subset="weather_date")
print("removed", before - len(df), "repeats")

# 3. turn the readings into numbers and put the unit in the column
df["prcp_in"] = pd.to_numeric(df["PRCP"], errors="coerce")
df["snow_in"] = pd.to_numeric(df["SNOW"], errors="coerce")
df["tmax_f"] = pd.to_numeric(df["TMAX"], errors="coerce")
df["tmin_f"] = pd.to_numeric(df["TMIN"], errors="coerce")
df["awnd_mph"] = pd.to_numeric(df["AWND"], errors="coerce")
for col in ["prcp_in", "snow_in", "tmax_f", "tmin_f", "awnd_mph"]:
    print(col, "-", df[col].isna().sum(), "missing")

# 4. if the low is greater than the high, that day's reading is wrong --> empty both
wrong = df["tmin_f"] > df["tmax_f"]
df.loc[wrong, ["tmin_f", "tmax_f"]] = pd.NA
print("emptied", wrong.sum(), "days where the low was greater than the high")

df = df[["weather_date", "prcp_in", "snow_in", "tmax_f", "tmin_f", "awnd_mph"]].sort_values("weather_date")
df.to_csv("data/clean/weather_clean.csv", index=False)
print("saved data/clean/weather_clean.csv with", len(df), "rows")
