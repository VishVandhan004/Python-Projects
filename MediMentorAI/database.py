import sqlite3  # SQLite database module for lightweight DB operations
from datetime import datetime  # To get current timestamp for saving records

DB_NAME = "medimentor_history.db"  # SQLite database file name

def init_db():
    """
    Initialize the database by creating the symptom_history table if it doesn't exist.
    This table stores user symptom queries and AI analysis results with timestamps.
    """
    conn = sqlite3.connect(DB_NAME)  # Connect to SQLite database file (creates if not exists)
    c = conn.cursor()  # Create a cursor object to execute SQL commands
    c.execute("""
        CREATE TABLE IF NOT EXISTS symptom_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each record, auto-incremented
            timestamp TEXT,                         -- Timestamp when record is saved (ISO format string)
            symptoms TEXT,                         -- User input symptoms text
            conditions TEXT,                       -- AI predicted probable conditions
            health_tips TEXT                       -- AI generated health tips
        )
    """)  # Execute SQL to create the table if not present already
    conn.commit()  # Save (commit) changes to the database
    conn.close()   # Close the connection to free resources

def save_symptom_history(symptoms, conditions, tips):
    """
    Insert a new symptom analysis record into the database with current timestamp.
    
    Parameters:
    - symptoms: string of symptoms input by user
    - conditions: string of probable conditions returned by AI
    - tips: string of health tips returned by AI
    """
    conn = sqlite3.connect(DB_NAME)  # Connect to DB
    c = conn.cursor()  # Cursor for DB operations
    # Insert a new row with current timestamp and provided data
    c.execute(
        "INSERT INTO symptom_history (timestamp, symptoms, conditions, health_tips) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), symptoms, conditions, tips)  # Use ISO 8601 timestamp
    )
    conn.commit()  # Commit changes
    conn.close()   # Close connection

def get_all_history():
    """
    Retrieve all saved symptom history records from the database,
    ordered by timestamp descending (most recent first).
    
    Returns:
    - List of tuples: (timestamp, symptoms, conditions, health_tips)
    """
    conn = sqlite3.connect(DB_NAME)  # Connect to DB
    c = conn.cursor()  # Cursor object
    c.execute("SELECT timestamp, symptoms, conditions, health_tips FROM symptom_history ORDER BY timestamp DESC")
    rows = c.fetchall()  # Fetch all rows from the query
    conn.close()  # Close connection
    return rows  # Return list of records
