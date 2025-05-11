from sqlalchemy import create_engine, text
import pymysql

# إعدادات الاتصال بقاعدة بيانات MySQL
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1JFbyRdzc63p',
    'database': 'olympics_db'
}

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
    
    # SQL statements to create tables
    create_tables_sql = """
    -- Drop existing tables if they exist
    SET FOREIGN_KEY_CHECKS = 0;
    DROP TABLE IF EXISTS results;
    DROP TABLE IF EXISTS teams;
    DROP TABLE IF EXISTS games;
    DROP TABLE IF EXISTS cities;
    DROP TABLE IF EXISTS events;
    DROP TABLE IF EXISTS sports;
    DROP TABLE IF EXISTS athletes;
    DROP TABLE IF EXISTS countries;
    SET FOREIGN_KEY_CHECKS = 1;

    -- Create countries table
    CREATE TABLE countries (
        country_id INT AUTO_INCREMENT PRIMARY KEY,
        NOC VARCHAR(3) NOT NULL UNIQUE,
        Region VARCHAR(100),
        Notes VARCHAR(255)
    );

    -- Create athletes table
    CREATE TABLE athletes (
        athlete_id INT PRIMARY KEY,
        athlete_name VARCHAR(255) NOT NULL,
        sex VARCHAR(1)
    );

    -- Create sports table
    CREATE TABLE sports (
        sport_id INT AUTO_INCREMENT PRIMARY KEY,
        sport_name VARCHAR(100) NOT NULL UNIQUE
    );

    -- Create events table
    CREATE TABLE events (
        event_id INT AUTO_INCREMENT PRIMARY KEY,
        event_name VARCHAR(255) NOT NULL,
        sport_id INT,
        FOREIGN KEY (sport_id) REFERENCES sports(sport_id)
    );

    -- Create cities table
    CREATE TABLE cities (
        city_id INT AUTO_INCREMENT PRIMARY KEY,
        city_name VARCHAR(100) NOT NULL UNIQUE
    );

    -- Create games table
    CREATE TABLE games (
        game_id INT AUTO_INCREMENT PRIMARY KEY,
        game_name VARCHAR(100) NOT NULL,
        year INT,
        season VARCHAR(20),
        city_id INT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id)
    );

    -- Create teams table
    CREATE TABLE teams (
        team_id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(255) NOT NULL UNIQUE
    );

    -- Create results table
    CREATE TABLE results (
        result_id INT AUTO_INCREMENT PRIMARY KEY,
        athlete_id INT,
        game_id INT,
        event_id INT,
        team_id INT,
        NOC VARCHAR(3),
        age FLOAT,
        height_cm FLOAT,
        weight_kg FLOAT,
        medal VARCHAR(20),
        FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
        FOREIGN KEY (game_id) REFERENCES games(game_id),
        FOREIGN KEY (event_id) REFERENCES events(event_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id),
        FOREIGN KEY (NOC) REFERENCES countries(NOC)
    );
    """

    try:
        engine = get_mysql_engine()
        with engine.connect() as conn:
            # Execute all SQL statements
            for statement in create_tables_sql.split(';'):
                if statement.strip():
                    conn.execute(text(statement))
            conn.commit()
        print("Database schema created successfully!")
    except Exception as e:
        print(f"Error creating database schema: {e}")
        raise

if __name__ == "__main__":
    create_schema()
