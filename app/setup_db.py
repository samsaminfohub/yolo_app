from database import Database

if __name__ == "__main__":
    print("Initializing database...")
    db = Database()
    db.create_tables()
    db.close()
    print("Database setup complete!")