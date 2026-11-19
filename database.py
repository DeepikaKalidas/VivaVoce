
import sqlite3

DB_NAME = "vivavoce.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS libraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                library_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                extracted_text TEXT NOT NULL,

                FOREIGN KEY (library_id)
                REFERENCES libraries(id)
                ON DELETE CASCADE
            )
        """)


def create_library(name):

    connection = get_connection()

    try:
        cursor = connection.execute(
            "INSERT OR IGNORE INTO libraries (name) VALUES (?)",
            (name,)
        )

        connection.commit()

        return cursor.rowcount == 1

    finally:
        connection.close()


def get_libraries():

    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT id, name FROM libraries ORDER BY created_at"
        )

        libraries = cursor.fetchall()

        return libraries

    finally:
        connection.close()
