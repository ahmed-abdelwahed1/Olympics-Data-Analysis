import pandas as pd
from sqlalchemy import create_engine, text
import pymysql
import os
from pathlib import Path
from config import MYSQL_CONFIG, TABLE_DEPENDENCIES, TABLE_SCHEMAS, ATHLETE_EVENTS_CSV, NOC_REGIONS_CSV

# Get the absolute path to the data directory
BASE_DIR = Path(__file__).resolve().parent.parent

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

def drop_all_tables(conn):
    """Drop all tables in the correct order to handle foreign key constraints"""
    print("Dropping existing tables...")
    try:
        # Disable foreign key checks
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Drop tables in reverse order of dependencies
        for table in TABLE_DEPENDENCIES:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
            print(f"Dropped table {table}")
            
        # Re-enable foreign key checks
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        print("All tables dropped successfully")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        # Make sure to re-enable foreign key checks even if there's an error
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        raise

def create_tables(engine):
    """Create all tables with proper schemas"""
    print("Creating tables...")
    try:
        with engine.connect() as conn:
            # Disable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Create tables in reverse dependency order
            for table in reversed(TABLE_DEPENDENCIES):
                conn.execute(text(TABLE_SCHEMAS[table]))
                print(f"Created table {table}")
            
            # Re-enable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Make sure to re-enable foreign key checks even if there's an error
        try:
            with engine.connect() as conn:
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        except:
            pass
        raise

def load_data_to_db():
    print("Starting data loading process...")

    # Load CSVs
    print("Loading CSV files...")
    try:
        if not os.path.exists(ATHLETE_EVENTS_CSV):
            raise FileNotFoundError(f"Athlete events CSV not found at: {ATHLETE_EVENTS_CSV}")
        if not os.path.exists(NOC_REGIONS_CSV):
            raise FileNotFoundError(f"NOC regions CSV not found at: {NOC_REGIONS_CSV}")
            
        athlete_events_df = pd.read_csv(ATHLETE_EVENTS_CSV)
        noc_df = pd.read_csv(NOC_REGIONS_CSV)
        print("CSV files loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading CSV files: {e}")
        return
    except Exception as e:
        print(f"Unexpected error loading CSV files: {e}")
        return

    try:
        engine = get_mysql_engine()
        conn = engine.connect()

        # Drop all existing tables
        drop_all_tables(conn)
        
        # Create tables with proper schemas
        create_tables(engine)

        # --- 1. Populate NOCs Table --- 
        print("Populating NOCs table...")
        if 'SGP' not in noc_df['NOC'].values:
            sgp_row = pd.DataFrame([{'NOC': 'SGP', 'region': 'Singapore', 'notes': 'Added manually'}])
            noc_df = pd.concat([noc_df, sgp_row], ignore_index=True)
        
        noc_to_insert = noc_df[['NOC', 'region', 'notes']].copy()
        noc_to_insert.rename(columns={'region': 'Region', 'notes': 'Notes'}, inplace=True)
        noc_to_insert.to_sql('countries', con=engine, if_exists='append', index=False)

        # --- 2. Populate Athletes Table --- 
        print("Populating Athletes table...")
        athletes_df = athlete_events_df[['ID', 'Name', 'Sex']].copy()
        athletes_df.drop_duplicates(subset=['ID'], inplace=True)
        athletes_df.rename(columns={'ID': 'athlete_id', 'Name': 'athlete_name', 'Sex': 'sex'}, inplace=True)
        athletes_df.to_sql('athletes', con=engine, if_exists='append', index=False)

        # --- 3. Populate Sports Table --- 
        print("Populating Sports table...")
        sports_df = athlete_events_df[['Sport']].drop_duplicates()
        sports_df.rename(columns={'Sport': 'sport_name'}, inplace=True)
        sports_df.to_sql('sports', con=engine, if_exists='append', index=False)

        # Retrieve SportID mapping
        sports_map = pd.read_sql("SELECT sport_id, sport_name FROM sports", con=engine)
        sports_map_dict = dict(zip(sports_map['sport_name'], sports_map['sport_id']))

        # --- 4. Populate Events Table --- 
        print("Populating Events table...")
        events_df = athlete_events_df[['Event', 'Sport']].drop_duplicates()
        events_df['sport_id'] = events_df['Sport'].map(sports_map_dict)
        events_df.rename(columns={'Event': 'event_name'}, inplace=True)
        events_df[['event_name', 'sport_id']].to_sql('events', con=engine, if_exists='append', index=False)

        # --- 5. Populate Cities Table ---
        print("Populating Cities table...")
        cities_df = athlete_events_df[['City']].drop_duplicates()
        cities_df.rename(columns={'City': 'city_name'}, inplace=True)
        cities_df.to_sql('cities', con=engine, if_exists='append', index=False)

        # --- 6. Populate Games Table --- 
        print("Populating Games table...")
        games_df = athlete_events_df[['Games', 'Year', 'Season', 'City']].drop_duplicates()
        games_df.rename(columns={'Games': 'game_name', 'Year': 'year', 'Season': 'season', 'City': 'city_name'}, inplace=True)
        cities_map = pd.read_sql("SELECT city_id, city_name FROM cities", con=engine)
        games_df['city_id'] = games_df['city_name'].map(dict(zip(cities_map['city_name'], cities_map['city_id'])))
        games_df[['game_name', 'year', 'season', 'city_id']].to_sql('games', con=engine, if_exists='append', index=False)

        # --- 7. Populate Teams Table ---
        print("Populating Teams table...")
        teams_df = athlete_events_df[['Team']].drop_duplicates()
        teams_df.rename(columns={'Team': 'team_name'}, inplace=True)
        teams_df.to_sql('teams', con=engine, if_exists='append', index=False)

        # --- 8. Populate Results Table ---
        print("Populating Results table...")
        # إعداد الخرائط
        events_map = pd.read_sql("SELECT event_id, event_name FROM events", con=engine)
        games_map = pd.read_sql("SELECT game_id, game_name FROM games", con=engine)
        teams_map = pd.read_sql("SELECT team_id, team_name FROM teams", con=engine)

        results_df = athlete_events_df[['ID', 'Games', 'Event', 'Team', 'NOC', 'Age', 'Height', 'Weight', 'Medal']].copy()
        results_df.rename(columns={'ID': 'athlete_id'}, inplace=True)
        results_df['game_id'] = results_df['Games'].map(dict(zip(games_map['game_name'], games_map['game_id'])))
        results_df['event_id'] = results_df['Event'].map(dict(zip(events_map['event_name'], events_map['event_id'])))
        results_df['team_id'] = results_df['Team'].map(dict(zip(teams_map['team_name'], teams_map['team_id'])))
        results_df['age'] = pd.to_numeric(results_df['Age'], errors='coerce')
        results_df['height_cm'] = pd.to_numeric(results_df['Height'], errors='coerce')
        results_df['weight_kg'] = pd.to_numeric(results_df['Weight'], errors='coerce')
        results_df['medal'] = results_df['Medal'].where(pd.notnull(results_df['Medal']), None)

        results_df[['athlete_id', 'game_id', 'event_id', 'team_id', 'NOC', 'age', 'height_cm', 'weight_kg', 'medal']].to_sql(
            'results', 
            con=engine, 
            if_exists='append', 
            index=False, 
            chunksize=10000
        )

        print("Data loading process finished successfully.")

    except Exception as e:
        print(f"Error during data loading: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_data_to_db()
