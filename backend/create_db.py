import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
import sys

# Load env from backend/.env
# Assuming script is run from project root, so we point to backend/.env
# But wait, run.py is in backend.
# Let's try to find .env relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)

db_url = os.getenv("DATABASE_URL")
if not db_url or not db_url.startswith("postgresql"):
    print("DATABASE_URL not set to postgresql in .env")
    sys.exit(0) 

# Parse URL (naive parsing)
# postgresql://user:password@host:port/dbname
try:
    from urllib.parse import urlparse
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    
    # Connect to 'postgres' system db to create our db
    print(f"Connecting to PostgreSQL at {hostname}:{port} as {username}...")
    con = psycopg2.connect(dbname='postgres', user=username, host=hostname, password=password, port=port)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    
    # Check if db exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database}'")
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Database '{database}' does not exist. Creating...")
        cursor.execute(f"CREATE DATABASE {database}")
        print(f"Database '{database}' created successfully.")
    else:
        print(f"Database '{database}' already exists.")
        
    cursor.close()
    con.close()
    
except Exception as e:
    print(f"Error checking/creating database: {e}")
    print("Please ensure PostgreSQL is running and credentials are correct.")
    # We will not exit with error code to avoid stopping the flow aggressively, 
    # but we will print the error so user sees it.
    sys.exit(1)
