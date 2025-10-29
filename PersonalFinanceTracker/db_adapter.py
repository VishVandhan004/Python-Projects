import os
import logging

def get_db_connection():
    """Get database connection - PostgreSQL on Railway, SQLite locally"""
    try:
        if os.environ.get('DATABASE_URL'):
            # Use PostgreSQL on Railway
            logging.debug("Using PostgreSQL on Railway")
            import psycopg2
            conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        else:
            # Use SQLite locally
            logging.debug("Using SQLite for local development")
            import sqlite3
            conn = sqlite3.connect('finance_tracker.db')
            conn.row_factory = sqlite3.Row
            
        logging.debug("Database connection successful")
        return conn
        
    except Exception as e:
        logging.critical(f"Database connection failed: {e}")
        raise