# runs integrate.sql in duckdb and saves the new table as a csv
import duckdb

with duckdb.connect("data/collision.duckdb") as con:
    with open("scripts/integrate.sql", "r") as f:
        con.sql(f.read())
    con.sql("COPY daily_integrated TO 'data/clean/daily_integrated.csv' (HEADER)")
    print(con.sql("SELECT count(*) AS days, min(date) AS first_day, max(date) AS last_day FROM daily_integrated").df())

print("saved data/clean/daily_integrated.csv")
