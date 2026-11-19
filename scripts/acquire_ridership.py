# downloads cta daily ridership totals, 2019-2024
# source: https://data.cityofchicago.org/Transportation/CTA-Ridership-Daily-Boarding-Totals/6iiy-9s97
from common import fetch

URL = "https://data.cityofchicago.org/resource/6iiy-9s97.csv"

params = {
    "$select": "service_date,day_type,bus,rail_boardings,total_rides",
    "$where": "service_date >= '2019-01-01T00:00:00' AND service_date < '2025-01-01T00:00:00'",
    "$order": "service_date",
    # one row per day so about 2,200 rows. the limit is just so nothing gets cut off.
    "$limit": 10000,
}

fetch(URL, params, "cta_ridership_2019_2024.csv")
