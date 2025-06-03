import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print("Connected to PostgreSQL database!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error connecting to PostgreSQL: {error}")

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS detections (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                detection_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                objects_detected JSONB,
                output_path VARCHAR(255),
                mlflow_run_id VARCHAR(255)
            )
            """,
        )
        
        try:
            cur = self.conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error creating tables: {error}")

    def insert_detection(self, filename, objects_detected, output_path, mlflow_run_id):
        sql_query = """
            INSERT INTO detections(filename, objects_detected, output_path, mlflow_run_id)
            VALUES(%s, %s, %s, %s)
            RETURNING id
        """
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql_query, (filename, objects_detected, output_path, mlflow_run_id))
            detection_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            return detection_id
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error inserting detection: {error}")
            return None

    def get_recent_detections(self, limit=5):
        sql_query = """
            SELECT id, filename, detection_time, objects_detected, output_path
            FROM detections
            ORDER BY detection_time DESC
            LIMIT %s
        """
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql_query, (limit,))
            detections = cur.fetchall()
            cur.close()
            return detections
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching detections: {error}")
            return []

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")