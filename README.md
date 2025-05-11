# Olympics Data Analysis

A comprehensive data analysis project for Olympic Games historical data, developed by Ahmed Abdelwahed as an assessment project for Stage One of the Data Engineering track @IEEE Mansoura Computer Society Chapter.

## Project Description

This project provides a robust system for analyzing historical Olympic Games data, including athlete performance, medal distributions, and participation trends across different sports and countries. It features a complete data pipeline from raw data processing to insightful visualizations, all backed by a well-structured MySQL database.

## Tech Stack

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white" />
<img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=matplotlib&logoColor=white" />
<img src="https://img.shields.io/badge/Seaborn-000000?style=flat-square&logo=seaborn&logoColor=white" />
<img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white" />

- **Programming Language**: Python 3.11
- **Data Processing**:
  - Pandas
  - NumPy
- **Database**:
  - MySQL
  - SQLAlchemy
- **Data Visualization**:
  - Matplotlib
  - Seaborn
- **Development Environment**:
  - JupyterLab
  - IPython Kernel

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

- `medals_by_country.png`: Top 10 countries by medal count
- `athlete_trends.png`: Athlete statistics over time
- `sports_distribution.png`: Distribution of sports and events
- `gender_distribution.png`: Gender participation trends

## Project Structure

```
Olympics-Data-Analysis/
├── analysis_results/     # Generated analysis visualizations
├── data/                 # Raw data files
│   ├── athlete_events.csv
│   └── noc_regions.csv
├── database/            # Database-related files
├── erd/                 # Entity Relationship Diagrams
├── notebooks/           # Jupyter notebook for initial exploration
├── scripts/             # Python scripts
│   ├── analyze.py       # Data analysis and visualization
│   ├── clean_data.py    # Data cleaning and processing
│   ├── config.py        # Configuration settings
│   ├── create_schema.py # Database schema creation
│   └── load_data.py     # Data loading utilities
└── task/                # Project requirements and description
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

### Table Descriptions

1. **countries**
   - Primary table for country information
   - Contains NOC (National Olympic Committee) codes and regions
   - Links to results through NOC code

2. **athletes**
   - Stores athlete information
   - Contains basic demographic data
   - Links to results through athlete_id

3. **sports**
   - Master table for all Olympic sports
   - Links to events through sport_id
   - Ensures consistent sport naming

4. **events**
   - Contains all Olympic events
   - Links to sports through sport_id
   - Links to results through event_id

5. **cities**
   - Stores host city information
   - Links to games through city_id
   - Ensures consistent city naming

6. **games**
   - Contains Olympic Games information
   - Includes year and season
   - Links to cities through city_id
   - Links to results through game_id

7. **teams**
   - Stores team information
   - Links to results through team_id
   - Handles team name consistency

8. **results**
   - Core table for all Olympic results
   - Contains performance metrics (age, height, weight)
   - Links to all other tables through foreign keys
   - Stores medal information

### Key Relationships

```mermaid
graph TD
    A[countries] -->|NOC| R[results]
    B[athletes] -->|athlete_id| R
    C[sports] -->|sport_id| D[events]
    D -->|event_id| R
    E[cities] -->|city_id| F[games]
    F -->|game_id| R
    G[teams] -->|team_id| R
```

## License

This project is part of the IEEE Mansoura Computer Society Chapter's Data Engineering track stage one evaluation process. All rights reserved.

## Additional Notes

- The project uses a MySQL database for data storage. Make sure MySQL is running before executing the scripts.
- Data files should be placed in the `data` directory before running the scripts.
- The analysis results are automatically saved in the `analysis_results` directory.
