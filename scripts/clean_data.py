import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import pymysql
from config import MYSQL_CONFIG, TABLE_DEPENDENCIES, TABLE_SCHEMAS

def get_mysql_engine():
    try:
        connection_str = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@" \
                        f"{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
        engine = create_engine(connection_str, echo=False)
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def load_data_from_db(engine):
    """Load all relevant data from the database"""
    print("Loading data from database...")
    
    queries = {
        'athletes': "SELECT * FROM athletes",
        'results': "SELECT * FROM results",
        'countries': "SELECT * FROM countries",
        'sports': "SELECT * FROM sports",
        'events': "SELECT * FROM events",
        'games': "SELECT * FROM games",
        'cities': "SELECT * FROM cities",
        'teams': "SELECT * FROM teams"
    }
    
    data = {}
    for table, query in queries.items():
        try:
            with engine.connect() as conn:
                data[table] = pd.read_sql(query, conn)
            print(f"Loaded {table} table")
        except Exception as e:
            print(f"Error loading {table} table: {e}")
            raise
    
    return data

def clean_athletes_data(df):
    """Clean athletes data"""
    print("\nCleaning athletes data...")
    
    # Handle missing values
    df['sex'] = df['sex'].fillna('Unknown')
    
    # Remove any duplicate athlete IDs
    df = df.drop_duplicates(subset=['athlete_id'])
    
    # Clean athlete names
    df['athlete_name'] = df['athlete_name'].str.strip()
    
    return df

def clean_results_data(df, athletes_df):
    """Clean results data"""
    print("\nCleaning results data...")
    
    # Handle missing values
    df['medal'] = df['medal'].fillna('No Medal')
    
    # Remove results with invalid athlete IDs
    valid_athlete_ids = athletes_df['athlete_id'].unique()
    df = df[df['athlete_id'].isin(valid_athlete_ids)]
    
    # Handle outliers in age
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    age_mean = df['age'].mean()
    age_std = df['age'].std()
    df.loc[df['age'] > age_mean + 3*age_std, 'age'] = np.nan
    df.loc[df['age'] < age_mean - 3*age_std, 'age'] = np.nan
    
    # Handle outliers in height
    df['height_cm'] = pd.to_numeric(df['height_cm'], errors='coerce')
    height_mean = df['height_cm'].mean()
    height_std = df['height_cm'].std()
    df.loc[df['height_cm'] > height_mean + 3*height_std, 'height_cm'] = np.nan
    df.loc[df['height_cm'] < height_mean - 3*height_std, 'height_cm'] = np.nan
    
    # Handle outliers in weight
    df['weight_kg'] = pd.to_numeric(df['weight_kg'], errors='coerce')
    weight_mean = df['weight_kg'].mean()
    weight_std = df['weight_kg'].std()
    df.loc[df['weight_kg'] > weight_mean + 3*weight_std, 'weight_kg'] = np.nan
    df.loc[df['weight_kg'] < weight_mean - 3*weight_std, 'weight_kg'] = np.nan
    
    return df

def clean_countries_data(df):
    """Clean countries data"""
    print("\nCleaning countries data...")
    
    # Handle missing values
    df['Region'] = df['Region'].fillna('Unknown')
    df['Notes'] = df['Notes'].fillna('')
    
    # Clean NOC codes
    df['NOC'] = df['NOC'].str.upper().str.strip()
    
    # Remove any duplicate NOC codes
    df = df.drop_duplicates(subset=['NOC'])
    
    return df

def clean_sports_data(df):
    """Clean sports data"""
    print("\nCleaning sports data...")
    
    # Clean sport names
    df['sport_name'] = df['sport_name'].str.strip()
    
    # Remove any duplicate sport names
    df = df.drop_duplicates(subset=['sport_name'])
    
    return df

def clean_events_data(df, sports_df):
    """Clean events data"""
    print("\nCleaning events data...")
    
    # Remove events with invalid sport IDs
    valid_sport_ids = sports_df['sport_id'].unique()
    df = df[df['sport_id'].isin(valid_sport_ids)]
    
    # Clean event names
    df['event_name'] = df['event_name'].str.strip()
    
    # Remove any duplicate event names within the same sport
    df = df.drop_duplicates(subset=['event_name', 'sport_id'])
    
    return df

def clean_games_data(df, cities_df):
    """Clean games data"""
    print("\nCleaning games data...")
    
    # Remove games with invalid city IDs
    valid_city_ids = cities_df['city_id'].unique()
    df = df[df['city_id'].isin(valid_city_ids)]
    
    # Clean game names
    df['game_name'] = df['game_name'].str.strip()
    
    # Clean season values
    df['season'] = df['season'].str.capitalize()
    
    return df

def clean_cities_data(df):
    """Clean cities data"""
    print("\nCleaning cities data...")
    
    # Clean city names
    df['city_name'] = df['city_name'].str.strip()
    
    # Remove any duplicate city names
    df = df.drop_duplicates(subset=['city_name'])
    
    return df

def clean_teams_data(df):
    """Clean teams data"""
    print("\nCleaning teams data...")
    
    # Clean team names
    df['team_name'] = df['team_name'].str.strip()
    
    # Remove any duplicate team names
    df = df.drop_duplicates(subset=['team_name'])
    
    return df

def save_cleaned_data(engine, cleaned_data):
    """Save cleaned data back to the database"""
    print("\nSaving cleaned data to database...")
    
    try:
        with engine.connect() as conn:
            # Disable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Drop all tables first
            for table in TABLE_DEPENDENCIES:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                    print(f"Dropped table {table}")
                except Exception as e:
                    print(f"Warning: Could not drop table {table}: {e}")
            
            # Create and populate tables in reverse order
            for table in reversed(TABLE_DEPENDENCIES):
                if table in cleaned_data:
                    print(f"Saving {table}...")
                    # Create table with proper schema
                    conn.execute(text(TABLE_SCHEMAS[table]))
                    
                    # Insert data
                    cleaned_data[table].to_sql(table, con=engine, if_exists='append', index=False)
            
            # Re-enable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
        print("All cleaned data saved successfully!")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")
        # Make sure to re-enable foreign key checks even if there's an error
        try:
            with engine.connect() as conn:
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        except:
            pass
        raise

def main():
    print("Starting data cleaning process...")
    
    try:
        # Get database connection
        engine = get_mysql_engine()
        
        # Load data
        data = load_data_from_db(engine)
        
        # Clean each table
        cleaned_data = {
            'athletes': clean_athletes_data(data['athletes']),
            'results': clean_results_data(data['results'], data['athletes']),
            'countries': clean_countries_data(data['countries']),
            'sports': clean_sports_data(data['sports']),
            'events': clean_events_data(data['events'], data['sports']),
            'games': clean_games_data(data['games'], data['cities']),
            'cities': clean_cities_data(data['cities']),
            'teams': clean_teams_data(data['teams'])
        }
        
        # Save cleaned data
        save_cleaned_data(engine, cleaned_data)
        
        print("\nData cleaning process completed successfully!")
        
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        raise

if __name__ == "__main__":
    main() 