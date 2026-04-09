import pandas as pd
import requests
import sqlite3
import json
import time

# Setup database
conn = sqlite3.connect('names.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS names (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        gender TEXT,
        count INTEGER,
        probability REAL,
        origin TEXT,
        meaning TEXT,
        style TEXT
    )
''')
conn.commit()


# Load CSV
df = pd.read_csv('name_gender_dataset.csv')

# Insert all names first if not already done
for _, row in df.iterrows():
    cursor.exectue('''
        INSERT OR IGNORE INTO names (name, gender, count, probability)
        VALUES (?, ?, ?, ?)
''', (row['Name'], row['Gender'], row['Count'], row['Probability']))
conn.commit()

print(f"Names loaded into database")