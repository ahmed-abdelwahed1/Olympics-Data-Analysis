# Olympics Data Analysis

A comprehensive data analysis project for Olympic Games historical data, developed as an evaluation project for Stage One @IEEEManCSC.

## Project Description

This project provides a robust system for analyzing historical Olympic Games data, including athlete performance, medal distributions, and participation trends across different sports and countries. It features a complete data pipeline from raw data processing to insightful visualizations, all backed by a well-structured MySQL database.

## Tech Stack

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
   - Update the database configuration in `scripts/config.py` with your MySQL credentials

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

The analysis results will be saved in the `analysis_results` directory as PNG files.

## Project Structure

```
Olympics-Data-Analysis/
├── analysis_results/     # Generated analysis visualizations
├── data/                 # Raw data files
├── database/            # Database-related files
├── erd/                 # Entity Relationship Diagrams
├── notebooks/           # Jupyter notebooks for analysis
├── results/             # Additional analysis results
├── scripts/             # Python scripts
│   ├── analyze.py       # Data analysis and visualization
│   ├── clean_data.py    # Data cleaning and processing
│   ├── config.py        # Configuration settings
│   ├── create_schema.py # Database schema creation
│   └── load_data.py     # Data loading utilities
└── task/                # Project requirements and documentation
```

## Key Features

1. **Data Pipeline**:
   - Automated data loading and cleaning
   - Robust error handling
   - Data integrity checks

2. **Analysis Capabilities**:
   - Medal distribution analysis by country
   - Athlete performance trends over time
   - Sports participation analysis
   - Gender distribution analysis

3. **Database Features**:
   - Normalized database schema
   - Foreign key constraints
   - Efficient data relationships

4. **Visualization Tools**:
   - Interactive plots
   - Statistical analysis
   - Trend visualization

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

Please ensure your code follows the existing style and includes appropriate documentation.

## License

This project is part of the IEEE Manchester Computer Science Club evaluation process. All rights reserved.

## Additional Notes

- The project uses a MySQL database for data storage. Make sure MySQL is running before executing the scripts.
- Data files should be placed in the `data` directory before running the scripts.
- The analysis results are automatically saved in the `analysis_results` directory.
- For detailed analysis, check the Jupyter notebooks in the `notebooks` directory.

## Contact

For questions or support, please contact the project maintainers or raise an issue in the repository.
