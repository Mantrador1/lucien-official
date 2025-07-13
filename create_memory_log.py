# -*- coding: utf-8 -*-
import psycopg2

DATABASE_URL = 'PASTE_YOUR_REAL_DATABASE_URL_HERE'  # <--- Replace with your actual DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute(\"""
CREATE TABLE IF NOT EXISTS memory_log (
    id UUID PRIMARY KEY,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    session_id TEXT NOT NULL,
    model TEXT NOT NULL
)
\""")
conn.commit()
conn.close()

print("? memory_log table created.")





