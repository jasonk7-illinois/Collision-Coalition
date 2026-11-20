-- joins the three sources into one table with one row per day
-- crashes has one row per crash, so first count them up per day
CREATE OR REPLACE TABLE daily_crashes AS
SELECT
    crash_date,
    -- get the crashes where the info is not blank
    COUNT(*) AS crash_count,
    -- get crashes where at least 1 person was injured
    COUNT(injuries_total) AS crashes_with_injury_info,
    SUM(CASE WHEN injuries_total > 0 THEN 1 ELSE 0 END) AS injury_crash_count,
    SUM(injuries_total) AS injuries_total,
    SUM(injuries_fatal) AS injuries_fatal,
    -- get what the officer recorded as the weather
    COUNT(weather_condition) AS crashes_with_weather_info,
    SUM(CASE WHEN weather_condition IN ('RAIN', 'SNOW', 'FREEZING RAIN/DRIZZLE', 'SLEET/HAIL', 'BLOWING SNOW')
             THEN 1 ELSE 0 END) AS crashes_reported_precip
FROM crashes
GROUP BY crash_date;

-- join  crashes, weather, ridership on date.
-- "full outer join" keeps a day even if one of the sources is missing it,the three has_ columns say which sources had that day
CREATE OR REPLACE TABLE daily_integrated AS
SELECT
    COALESCE(dc.crash_date, w.weather_date, r.service_date) AS date,
    r.day_type,
    dc.crash_count,
    dc.crashes_with_injury_info,
    dc.injury_crash_count,
    dc.injuries_total,
    dc.injuries_fatal,
    dc.crashes_with_weather_info,
    dc.crashes_reported_precip,
    w.prcp_in,
    w.snow_in,
    w.tmax_f,
    w.tmin_f,
    w.awnd_mph,
    r.bus_rides,
    r.rail_rides,
    r.total_rides,
    dc.crash_date IS NOT NULL AS has_crashes,
    w.weather_date IS NOT NULL AS has_weather,
    r.service_date IS NOT NULL AS has_ridership
FROM daily_crashes dc
FULL OUTER JOIN weather w
    ON dc.crash_date = w.weather_date
FULL OUTER JOIN ridership r
    ON COALESCE(dc.crash_date, w.weather_date) = r.service_date
ORDER BY date;
