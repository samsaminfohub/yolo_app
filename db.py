
import psycopg2
from datetime import datetime
from config import DB_CONFIG

def log_detection(label, source_file):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO detections (label, source_file, detected_at)
        VALUES (%s, %s, %s)
    """, (label, source_file, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
