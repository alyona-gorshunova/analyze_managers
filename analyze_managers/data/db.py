import psycopg2

from analyze_managers.config import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USER,
)


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        """Get access to the database connection"""
        if not self.connection:
            self.connect()
        return self.connection

    def connect(self):
        """Establish connection to the PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=DATABASE_HOST,
                database=DATABASE_NAME,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                port=DATABASE_PORT,
            )
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager enter"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
