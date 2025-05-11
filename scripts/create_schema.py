from sqlalchemy import create_engine, text
import pymysql
from config import MYSQL_CONFIG, TABLE_DEPENDENCIES, TABLE_SCHEMAS

def get_mysql_engine():
    try:
        connection_str = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@" \
                        f"{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
        engine = create_engine(connection_str, echo=False)
        # Test the connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def create_schema():
    """Create the database schema for the Olympics database"""
    print("Creating database schema...")
    
    try:
        engine = get_mysql_engine()
        with engine.connect() as conn:
            # Disable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Drop existing tables in dependency order
            for table in TABLE_DEPENDENCIES:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"Dropped table {table}")
            
            # Create tables in reverse dependency order
            for table in reversed(TABLE_DEPENDENCIES):
                conn.execute(text(TABLE_SCHEMAS[table]))
                print(f"Created table {table}")
            
            # Re-enable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
        print("Database schema created successfully!")
    except Exception as e:
        print(f"Error creating database schema: {e}")
        # Make sure to re-enable foreign key checks even if there's an error
        try:
            with engine.connect() as conn:
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        except:
            pass
        raise

if __name__ == "__main__":
    create_schema()
