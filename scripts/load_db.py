# makes the duckdb database and loads three cleaned csv files into it.
import duckdb

with duckdb.connect("data/collision.duckdb") as con:
    with open("scripts/schema.sql", "r") as f:
        ddl = f.read()
        con.sql(ddl)

    con.sql("COPY weather FROM 'data/clean/weather_clean.csv' (HEADER)")
    con.sql("COPY ridership FROM 'data/clean/ridership_clean.csv' (HEADER)")
    con.sql("COPY crashes FROM 'data/clean/crashes_clean.csv' (HEADER)")

    # print how many rows are in each table so we can see it worked
    print(con.sql("SELECT 'weather' AS table_name, count(*) AS row_count FROM weather UNION ALL SELECT 'ridership', count(*) FROM ridership UNION ALL SELECT 'crashes', count(*) FROM crashes").df())

print("database saved at data/collision.duckdb")
