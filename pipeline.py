import requests
import pandas as pd

# Define the API endpoint
api_url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 35.6895,
    "longitude": 139.6917,
    "hourly": "temperature_2m"
}

# Make a GET request to fetch data
response = requests.get(api_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
else:
    print("Failed to fetch data:", response.status_code)
    
    
# Extract the relevant data from the JSON response
temperature_data = data['hourly']['temperature_2m']
timestamps = data['hourly']['time']

# Create a DataFrame
df = pd.DataFrame({'timestamp': timestamps, 'temperature': temperature_data})

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(df.head())

import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="api_data", user="postgres", password="Q^4.1nf0r", host= "localhost"
)
cur = conn.cursor()

# Insert DataFrame into PostgreSQL
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO weather_data (timestamp, temperature) VALUES (%s, %s)",
        (row['timestamp'], row['temperature'])
    )

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()
print("Data inserted into PostgreSQL successfully!")
