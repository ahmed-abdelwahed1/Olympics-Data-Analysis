# Olympics Data Analysis

A comprehensive data analysis project for Olympic Games historical data, developed by Ahmed Abdelwahed as an assessment project for Stage One of the Data Engineering track @IEEE Mansoura Computer Society Chapter.

## Project Description

This project provides a robust system for analyzing historical Olympic Games data, including athlete performance, medal distributions, and participation trends across different sports and countries. It features a complete data pipeline from raw data processing to insightful visualizations, all backed by a well-structured MySQL database.

## Dataset Source

The dataset used in this project is sourced from Kaggle:
[120 Years of Olympic History: Athletes and Results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

This dataset contains historical data on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016. It includes information about athletes, events, medals, and more.

## Tech Stack

<p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white"/>
    <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
    <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>
    <img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=matplotlib&logoColor=white"/>
    <img src="https://img.shields.io/badge/Seaborn-000000?style=flat-square&logo=seaborn&logoColor=white"/>
    <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white"/>
</p>

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Olympics-Data-Analysis.git
   cd Olympics-Data-Analysis
   ```

2. Create and activate the Conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate olympics-project
   ```

3. Set up MySQL database:
   - Install MySQL if not already installed
   - Create a new database named `olympics_db`
   - Update the database configuration in `scripts/config.py` with your MySQL credentials:

     ```python
     MYSQL_CONFIG = {
         'host': 'localhost',
         'port': 3306,
         'user': 'your_username',
         'password': 'your_password',
         'database': 'olympics_db'
     }
     ```

## Usage

The project follows a sequential workflow:

1. Create the database schema:

   ```bash
   python scripts/create_schema.py
   ```

2. Load the initial data:

   ```bash
   python scripts/load_data.py
   ```

3. Clean and process the data:

   ```bash
   python scripts/clean_data.py
   ```

4. Run the analysis:

   ```bash
   python scripts/analyze.py
   ```

The analysis results will be saved in the `analysis_results` directory as PNG files:

## Analysis Results

The project generates several insightful visualizations:

### Medal Distribution by Country

![Medal Distribution](analysis_results/medals_by_country.png)
*Top 10 countries by medal count, showing the distribution of Gold, Silver, and Bronze medals*

### Athlete Performance Trends

![Athlete Trends](analysis_results/athlete_trends.png)
*Historical trends in athlete statistics including age, height, and weight*

### Sports Distribution

![Sports Distribution](analysis_results/sports_distribution.png)
*Distribution of sports and events across the Olympic Games*

### Gender Participation

![Gender Distribution](analysis_results/gender_distribution.png)
*Evolution of gender participation in the Olympic Games over time*

## Project Structure

## Data Pipeline Flowchart

Below is a high-level flowchart illustrating the data pipeline, ETL process, and analysis workflow for this project:

```mermaid
flowchart TD
    %% Data Sources
    subgraph "Data Sources"
        A1["athlete_events.csv"]:::doc
        A2["noc_regions.csv"]:::doc
    end

    %% Environment
    subgraph "Conda Environment"
        Env["environment.yml"]:::env
    end

    %% Configuration
    subgraph "Configuration"
        Config["config.py"]:::config
    end

    %% Database
    subgraph "Database: MySQL (olympics_db)"
        DBraw["Raw Tables\n(countries, athletes,\nsports, events,\ncities, games,\nteams, results)"]:::db
        DBclean["Cleaned Tables"]:::db
    end

    %% ETL Scripts
    subgraph "ETL Scripts"
        CS["create_schema.py\n(pymysql)"]:::script
        LD["load_data.py\n(pandas, sqlalchemy)"]:::script
        CD["clean_data.py\n(pandas)"]:::script
    end

    %% Data Validation
    subgraph "Data Validation"
        DV["validate_data.py\n(pandas)"]:::script
    end

    %% Analysis & Notebook
    subgraph "Analysis"
        AN["analyze.py\n(matplotlib, seaborn)"]:::script
        NB["data_exploration.ipynb"]:::notebook
    end

    %% Data Visualization
    subgraph "Data Visualization"
        DViz["visualize.py\n(matplotlib, seaborn)"]:::script
    end

    %% Outputs
    subgraph "Outputs"
        AR["analysis_results/*.png"]:::doc
        PPT["Olympics Data Analysis.pptx"]:::doc
    end

    %% Data Flow
    A1 -->|input| LD
    A2 -->|input| LD
    Config -->|credentials| CS
    CS -->|create schema| DBraw
    LD -->|load raw data| DBraw
    DBraw -->|raw data| CD
    CD -->|write cleaned data| DBclean
    DBclean -->|validated data| DV
    DV -->|validated data| DBclean
    DBclean -->|cleaned data| AN
    AN -->|produce PNGs| AR
    AR -->|used in| PPT
    NB <-->|explore/query| DBclean
    AN -->|data for visualization| DViz
    DViz -->|visualizations| AR

    %% Environment dependencies
    Env -.-> CS
    Env -.-> LD
    Env -.-> CD
    Env -.-> DV
    Env -.-> AN
    Env -.-> DViz
    Env -.-> NB

    %% Click Events
    click A1 "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/data/athlete_events.csv"
    click A2 "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/data/noc_regions.csv"
    click Env "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/environment.yml"
    click Config "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/config.py"
    click CS "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/create_schema.py"
    click LD "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/load_data.py"
    click CD "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/clean_data.py"
    click DV "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/validate_data.py"
    click AN "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/analyze.py"
    click DViz "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/scripts/visualize.py"
    click NB "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/notebooks/data_exploration.ipynb"
    click AR "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/tree/main/analysis_results/"
    click PPT "https://github.com/ahmed-abdelwahed1/olympics-data-analysis/blob/main/presentation/Olympics Data Analysis.pptx"

    %% Styles
    classDef db fill:#bbdefb,stroke:#0d47a1,color:#0d47a1,stroke-width:1px;
    classDef script fill:#c8e6c9,stroke:#2e7d32,color:#2e7d32,stroke-width:1px;
    classDef doc fill:#ffe0b2,stroke:#ef6c00,color:#bf360c,stroke-width:1px;
    classDef env fill:#e1bee7,stroke:#6a1b9a,color:#4a148c,stroke-width:1px;
    classDef config fill:#c5cae9,stroke:#283593,color:#1a237e,stroke-width:1px;
    classDef notebook fill:#d1c4e9,stroke:#512da8,color:#311b92,stroke-width:1px;
```

## Database Schema

The project uses a normalized database schema with the following structure:

### Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    countries ||--o{ results : "has"
    countries {
        int country_id PK
        varchar NOC UK
        varchar Region
        varchar Notes
    }
    
    athletes ||--o{ results : "participates"
    athletes {
        int athlete_id PK
        varchar athlete_name
        varchar sex
    }
    
    sports ||--o{ events : "contains"
    sports {
        int sport_id PK
        varchar sport_name UK
    }
    
    events ||--o{ results : "has"
    events {
        int event_id PK
        varchar event_name
        int sport_id FK
    }
    
    cities ||--o{ games : "hosts"
    cities {
        int city_id PK
        varchar city_name UK
    }
    
    games ||--o{ results : "includes"
    games {
        int game_id PK
        varchar game_name
        int year
        varchar season
        int city_id FK
    }
    
    teams ||--o{ results : "has"
    teams {
        int team_id PK
        varchar team_name UK
    }
    
    results {
        int result_id PK
        int athlete_id FK
        int game_id FK
        int event_id FK
        int team_id FK
        varchar NOC FK
        float age
        float height_cm
        float weight_kg
        varchar medal
    }
```

### Database Relationships

The database schema implements a comprehensive set of relationships that maintain referential integrity and support efficient data querying:

#### One-to-Many (1:N) Relationships

- **Countries → Results**: A country (identified by NOC) can have multiple Olympic results
- **Athletes → Results**: An athlete can participate in multiple Olympic events
- **Sports → Events**: A sport can contain multiple competitive events
- **Events → Results**: An event can have multiple participant results
- **Cities → Games**: A city can host multiple Olympic Games (e.g., London hosted in 1908, 1948, and 2012)
- **Games → Results**: An Olympic Games can contain multiple event results
- **Teams → Results**: A team can participate in multiple events

#### Many-to-Many (M:N) Relationships

The following many-to-many relationships are implemented through the results table as a junction table:

- **Athletes ↔ Events**:
  - An athlete can participate in multiple events
  - An event can have multiple participating athletes
  - Junction: results table with athlete_id and event_id
- **Athletes ↔ Games**:
  - An athlete can compete in multiple Olympic Games
  - An Olympic Games can have multiple participating athletes
  - Junction: results table with athlete_id and game_id
- **Teams ↔ Events**:
  - A team can participate in multiple events
  - An event can have multiple participating teams
  - Junction: results table with team_id and event_id

#### One-to-One (1:1) Relationships

- **Events ↔ Sports**: Each event is uniquely associated with one sport (enforced by event.sport_id foreign key)

## License

This project is part of the IEEE Mansoura Computer Society Chapter's Data Engineering track stage one evaluation process. All rights reserved.
