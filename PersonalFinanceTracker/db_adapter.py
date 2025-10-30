import os
import logging

def get_db_connection():
    try:
        # ALWAYS use PostgreSQL on Railway, never SQLite
        logging.debug("Using PostgreSQL on Railway")
        import psycopg2
        
        # Get DATABASE_URL from Railway environment
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # Parse the database URL for proper connection
            import urllib.parse as urlparse
            
            # Parse the database URL
            url = urlparse.urlparse(database_url)
            
            # Extract connection parameters
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port
            
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                sslmode='require'
            )
            logging.debug("PostgreSQL connection successful")
            return conn
        else:
            # This should never happen on Railway, but fallback
            raise Exception("DATABASE_URL not found - cannot connect to database")
            
    except Exception as e:
        logging.critical(f"Database connection failed: {e}")
        # Don't fall back to SQLite on Railway
        raise Exception(f"Cannot connect to database: {e}")