import psycopg2

conn = psycopg2.connect(
    dbname="api_data", user="postgres", password="Q^4.1nf0r", host="localhost"
)
cur = conn.cursor()

cur.execute("SELECT * FROM weather_data WHERE timestamp > NOW() - INTERVAL '1 day'")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
