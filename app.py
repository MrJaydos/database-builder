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

# Enrich in batches
BATCH_SIZE = 20
OLLAMA_URL = 'http://192.168.68.73:11434/api/generate'

def enrich_batch(names_batch):
    names_list = ', '.join([n for n in names_batch])
    prompt = f"""For each of these baby names return a JSON array where each object has exactly these fields: name, origin, meaning, style(one of: Classic, Modern, Contemporary, Unique, Cultural).
Names: {names_list}
Return only a valid JSON array, no other text, no markdown."""
    

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
            }, timeout=60)
        return json.loads(response.json()['response'])
    except Exception as e:
        print(f"Error: {e}")
        return None