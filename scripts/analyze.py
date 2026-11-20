# analysis for research questions 1 and 2
# run from the project folder: python scripts/analyze.py
import pandas as pd

df = pd.read_csv("data/clean/daily_integrated.csv")
df["year"] = pd.to_datetime(df["date"]).dt.year
df["injury_share"] = df["injury_crash_count"] / df["crashes_with_injury_info"]

# Q1: weather vs crashes
# each day gets one label, snow overrides rain if both happened
df["weather_group"] = "Dry, above freezing"
df.loc[df["tmin_f"] <= 32, "weather_group"] = "Dry, freezing"
df.loc[df["prcp_in"] >= 0.1, "weather_group"] = "Rain"
df.loc[df["snow_in"] >= 0.1, "weather_group"] = "Snow"
df.loc[df["prcp_in"].isna() | df["tmin_f"].isna(), "weather_group"] = pd.NA

q1 = df.groupby("weather_group").agg(
    days=("date", "count"),
    mean_crashes=("crash_count", "mean"),
    median_crashes=("crash_count", "median"),
    mean_injury_share=("injury_share", "mean"),
).round(3)
q1.to_csv("results/crashes_by_weather.csv")
print(q1)

chart = q1["mean_crashes"].plot(kind="bar", ylabel="Avg crashes per day", xlabel="",
                                title="Chicago crashes per day by weather (2019-2024)", rot=0)
chart.get_figure().savefig("results/crashes_by_weather.png", bbox_inches="tight")
chart.get_figure().clear()

# Q2: CTA ridership vs crashes
# 2020-2021 split out since covid dropped ridership a lot
df["period"] = "2019, 2022-2024"
df.loc[df["year"].isin([2020, 2021]), "period"] = "2020-2021 (covid)"

rows = []
for period in df["period"].unique():
    for day_type in ["WEEKDAY", "SATURDAY", "SUNDAY_HOLIDAY"]:
        part = df[(df["period"] == period) & (df["day_type"] == day_type)]
        rows.append({
            "period": period,
            "day_type": day_type,
            "days": len(part),
            "mean_total_rides": round(part["total_rides"].mean()),
            "mean_crashes": round(part["crash_count"].mean(), 1),
            "correlation_rides_vs_crashes": round(part["total_rides"].corr(part["crash_count"]), 3),
        })
q2 = pd.DataFrame(rows)
q2.to_csv("results/ridership_vs_crashes.csv", index=False)
print(q2)

chart = df.plot(kind="scatter", x="total_rides", y="crash_count", s=5, alpha=0.4,
                xlabel="CTA rides per day", ylabel="Crashes per day",
                title="CTA ridership vs crashes per day (2019-2024)")
chart.get_figure().savefig("results/ridership_vs_crashes.png", bbox_inches="tight")

print("done, results saved to results/")
