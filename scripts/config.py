import os
from pathlib import Path

# Database Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1JFbyRdzc63p',
    'database': 'olympics_db'
}

# File Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR, "data")
ATHLETE_EVENTS_CSV = os.path.join(DATA_DIR, "athlete_events.csv")
NOC_REGIONS_CSV = os.path.join(DATA_DIR, "noc_regions.csv")

# Table Dependencies
TABLE_DEPENDENCIES = [
    'results',    # Most dependent table
    'teams',
    'games',
    'cities',
    'events',
    'sports',
    'athletes',
    'countries'   # Least dependent table
]

# Table Schemas
TABLE_SCHEMAS = {
    'countries': """
        CREATE TABLE countries (
            country_id INT AUTO_INCREMENT PRIMARY KEY,
            NOC VARCHAR(3) NOT NULL UNIQUE,
            Region VARCHAR(100),
            Notes VARCHAR(255)
        )
    """,
    'athletes': """
        CREATE TABLE athletes (
            athlete_id INT PRIMARY KEY,
            athlete_name VARCHAR(255) NOT NULL,
            sex VARCHAR(1)
        )
    """,
    'sports': """
        CREATE TABLE sports (
            sport_id INT AUTO_INCREMENT PRIMARY KEY,
            sport_name VARCHAR(100) NOT NULL UNIQUE
        )
    """,
    'events': """
        CREATE TABLE events (
            event_id INT AUTO_INCREMENT PRIMARY KEY,
            event_name VARCHAR(255) NOT NULL,
            sport_id INT,
            FOREIGN KEY (sport_id) REFERENCES sports(sport_id)
        )
    """,
    'cities': """
        CREATE TABLE cities (
            city_id INT AUTO_INCREMENT PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL UNIQUE
        )
    """,
    'games': """
        CREATE TABLE games (
            game_id INT AUTO_INCREMENT PRIMARY KEY,
            game_name VARCHAR(100) NOT NULL,
            year INT,
            season VARCHAR(20),
            city_id INT,
            FOREIGN KEY (city_id) REFERENCES cities(city_id)
        )
    """,
    'teams': """
        CREATE TABLE teams (
            team_id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL UNIQUE
        )
    """,
    'results': """
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
        )
    """
} 