import pandas as pd
from sqlalchemy import create_engine, text
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
from config import MYSQL_CONFIG
import os
from pathlib import Path

# Create analysis_results directory
ANALYSIS_DIR = Path(__file__).resolve().parent.parent / "analysis_results"
ANALYSIS_DIR.mkdir(exist_ok=True)

def get_mysql_engine():
    try:
        connection_str = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@" \
                        f"{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
        engine = create_engine(connection_str, echo=False)
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def execute_query(engine, query):
    """Execute a SQL query and return results as a pandas DataFrame"""
    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error executing query: {e}")
        raise

def analyze_medals_by_country():
    """Analyze medal counts by country"""
    query = """
    SELECT 
        c.Region as Country,
        COUNT(CASE WHEN r.medal = 'Gold' THEN 1 END) as Gold,
        COUNT(CASE WHEN r.medal = 'Silver' THEN 1 END) as Silver,
        COUNT(CASE WHEN r.medal = 'Bronze' THEN 1 END) as Bronze,
        COUNT(r.medal) as Total_Medals
    FROM results r
    JOIN countries c ON r.NOC = c.NOC
    WHERE r.medal IS NOT NULL
    GROUP BY c.Region
    ORDER BY Total_Medals DESC
    LIMIT 10;
    """
    
    df = execute_query(get_mysql_engine(), query)
    print("\nTop 10 Countries by Total Medals:")
    print(df)
    
    # Create a bar plot
    plt.figure(figsize=(12, 6))
    df_melted = pd.melt(df, id_vars=['Country'], 
                        value_vars=['Gold', 'Silver', 'Bronze'],
                        var_name='Medal Type', value_name='Count')
    
    # Define medal colors
    medal_colors = {
        'Gold': '#FFD700',    # Gold color
        'Silver': '#C0C0C0',  # Silver color
        'Bronze': '#CD7F32'   # Bronze color
    }
    
    # Create the bar plot with custom colors
    sns.barplot(
        data=df_melted,
        x='Country',
        y='Count',
        hue='Medal Type',
        palette=medal_colors
    )
    
    plt.title('Medal Distribution for Top 10 Countries')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(ANALYSIS_DIR / 'medals_by_country.png')
    plt.close()

def analyze_athlete_performance():
    """Analyze athlete performance over time"""
    query = """
    SELECT 
        g.year,
        g.season,
        COUNT(DISTINCT r.athlete_id) as Total_Athletes,
        AVG(r.age) as Avg_Age,
        AVG(r.height_cm) as Avg_Height,
        AVG(r.weight_kg) as Avg_Weight
    FROM results r
    JOIN games g ON r.game_id = g.game_id
    GROUP BY g.year, g.season
    ORDER BY g.year;
    """
    
    df = execute_query(get_mysql_engine(), query)
    print("\nAthlete Statistics Over Time:")
    print(df)
    
    # Create line plots for trends
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(df['year'], df['Total_Athletes'])
    plt.title('Number of Athletes Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Athletes')
    
    plt.subplot(2, 2, 2)
    plt.plot(df['year'], df['Avg_Age'])
    plt.title('Average Age Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average Age')
    
    plt.subplot(2, 2, 3)
    plt.plot(df['year'], df['Avg_Height'])
    plt.title('Average Height Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average Height (cm)')
    
    plt.subplot(2, 2, 4)
    plt.plot(df['year'], df['Avg_Weight'])
    plt.title('Average Weight Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average Weight (kg)')
    
    plt.tight_layout()
    plt.savefig(ANALYSIS_DIR / 'athlete_trends.png')
    plt.close()

def analyze_sports_distribution():
    """Analyze the distribution of sports and events"""
    query = """
    SELECT 
        s.sport_name,
        COUNT(DISTINCT e.event_id) as Event_Count,
        COUNT(DISTINCT r.athlete_id) as Athlete_Count
    FROM sports s
    LEFT JOIN events e ON s.sport_id = e.sport_id
    LEFT JOIN results r ON e.event_id = r.event_id
    GROUP BY s.sport_name
    ORDER BY Event_Count DESC;
    """
    
    df = execute_query(get_mysql_engine(), query)
    print("\nSports Distribution:")
    print(df)
    
    # Create a horizontal bar plot
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df.head(15), y='sport_name', x='Event_Count')
    plt.title('Top 15 Sports by Number of Events')
    plt.xlabel('Number of Events')
    plt.ylabel('Sport')
    plt.tight_layout()
    plt.savefig(ANALYSIS_DIR / 'sports_distribution.png')
    plt.close()

def analyze_gender_distribution():
    """Analyze gender participation over time"""
    query = """
    SELECT 
        g.year,
        g.season,
        a.sex,
        COUNT(DISTINCT r.athlete_id) as Athlete_Count
    FROM results r
    JOIN games g ON r.game_id = g.game_id
    JOIN athletes a ON r.athlete_id = a.athlete_id
    GROUP BY g.year, g.season, a.sex
    ORDER BY g.year;
    """
    
    df = execute_query(get_mysql_engine(), query)
    print("\nGender Distribution Over Time:")
    print(df)
    
    # Create a line plot
    plt.figure(figsize=(12, 6))
    for sex in df['sex'].unique():
        sex_data = df[df['sex'] == sex]
        plt.plot(sex_data['year'], sex_data['Athlete_Count'], label=sex)
    
    plt.title('Gender Participation Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Athletes')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ANALYSIS_DIR / 'gender_distribution.png')
    plt.close()

def main():
    print("Starting data analysis...")
    
    try:
        # Run all analyses
        analyze_medals_by_country()
        analyze_athlete_performance()
        analyze_sports_distribution()
        analyze_gender_distribution()
        
        print("\nData analysis completed successfully!")
        print(f"Analysis results have been saved to: {ANALYSIS_DIR}")
        
    except Exception as e:
        print(f"Error during data analysis: {e}")
        raise

if __name__ == "__main__":
    main()
