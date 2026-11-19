# downloads noaa daily weather for chicago o'hare, 2019-2024
# source: https://www.ncei.noaa.gov/access/services/data/v1
from common import fetch

URL = "https://www.ncei.noaa.gov/access/services/data/v1"

params = {
    "dataset": "daily-summaries",
    "stations": "USW00094846",  # this is the o'hare airport station
    "startDate": "2019-01-01",
    "endDate": "2024-12-31",
    "dataTypes": "PRCP,SNOW,TMAX,TMIN,AWND",  # rain, snow, high temp, low temp, wind
    "units": "standard",  # inches, fahrenheit, mph
    "format": "csv",
}

fetch(URL, params, "weather_ohare_2019_2024.csv")
