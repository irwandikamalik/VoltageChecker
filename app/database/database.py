import sqlite3
import os



class Database:

    def __init__(self, db_path="data/voltage_checker.db"):
        self.db_path = db_path

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)


    def create_tables(self):
        cursor = self.connection.cursor()

        # TABLE OPERATORS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operator_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            )
        """)

        # TABLE MODELS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT UNIQUE NOT NULL,
                voltage_lower REAL NOT NULL,
                voltage_upper REAL NOT NULL,
                current_lower REAL NOT NULL,
                current_upper REAL NOT NULL
            )
        """)

        # TABLE ADMIN
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            )
        """)

        # TABLE BATCH SERIAL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS batches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_code TEXT UNIQUE NOT NULL,
                model_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                current_sequence INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def close(self):
        self.connection.close()