-- one table of cleaned data per source
-- all three tables match to each other through matching dates

DROP TABLE IF EXISTS daily_integrated;
DROP TABLE IF EXISTS daily_crashes;
DROP TABLE IF EXISTS crashes;
DROP TABLE IF EXISTS weather;
DROP TABLE IF EXISTS ridership;

CREATE TABLE weather (
    weather_date DATE PRIMARY KEY,
    prcp_in      DOUBLE,
    snow_in      DOUBLE,
    tmax_f       DOUBLE, 
    tmin_f       DOUBLE, 
    awnd_mph     DOUBLE
);

CREATE TABLE ridership (
    service_date DATE PRIMARY KEY,
    day_type     VARCHAR NOT NULL,
    bus_rides    BIGINT,
    rail_rides   BIGINT,
    total_rides  BIGINT
);

CREATE TABLE crashes (
    crash_record_id      VARCHAR PRIMARY KEY,
    crash_timestamp      TIMESTAMP NOT NULL,
    crash_date           DATE NOT NULL,
    weather_condition    VARCHAR,
    roadway_surface_cond VARCHAR,
    lighting_condition   VARCHAR,
    most_severe_injury   VARCHAR,
    injuries_total       INTEGER,
    injuries_fatal       INTEGER,
    posted_speed_limit   INTEGER
);
