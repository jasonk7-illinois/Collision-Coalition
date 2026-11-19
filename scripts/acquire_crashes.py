# downloads chicago traffic crashes for 2019-2024, one csv per year
# source: https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
from common import fetch

URL = "https://data.cityofchicago.org/resource/85ca-t3if.csv"

# only the columns from our project plan. no names or locations, nothing personal.
COLUMNS = "crash_record_id,crash_date,weather_condition,roadway_surface_cond,lighting_condition,most_severe_injury,injuries_total,injuries_fatal,posted_speed_limit"

for year in [2019, 2020, 2021, 2022, 2023, 2024]:
    params = {
        "$select": COLUMNS,
        # only crashes from this one year
        "$where": "crash_date >= '" + str(year) + "-01-01T00:00:00' AND crash_date < '" + str(year + 1) + "-01-01T00:00:00'",
        # always the same order, so the same data gives the same file and the same hash
        "$order": "crash_date, crash_record_id",
        # the api only gives 1,000 rows unless you ask for more. a year is about 110,000.
        "$limit": 1000000,
    }
    # all six years in one file would be about 146 MB, too big for github, so one file per year
    fetch(URL, params, "crashes_" + str(year) + ".csv")
