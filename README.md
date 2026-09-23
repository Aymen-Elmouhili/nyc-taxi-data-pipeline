# NYC Taxi Data Pipeline

## 📌 Overview

This project implements an end-to-end data pipeline for processing NYC Yellow Taxi trip data.

The objective is to build a reproducible Data Engineering pipeline that extracts raw Parquet data, loads it into PostgreSQL, transforms it into a dimensional data warehouse, and provides an analytical layer for querying the processed data.

## 🏗️ Architecture

```text
NYC Taxi Parquet Data
        │
        ▼
   Extract / Load
        │
        ▼
 PostgreSQL - RAW
        │
        ▼
    Transform
        │
        ▼
 PostgreSQL - WAREHOUSE
        │
        ├── dim_datetime
        ├── dim_location
        └── fact_trips
        │
        ▼
    Analytics
        │
        ▼
     Jupyter
     Notebooks
```

## 📂 Project Structure

```text
nyc-taxi-data-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   └── 02_analytics.ipynb
│
├── src/
│   ├── config/
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   └── settings.py
│   │
│   ├── load/
│   │   └── load_data.py
│   │
│   ├── transform/
│   │   └── transform_data.py
│   │
│   ├── analytics/
│   │   └── queries.py
│   │
│   └── pipeline.py
│
├── sql/
├── tests/
├── logs/
│
├── .env
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 🛠️ Technologies

* Python
* PostgreSQL
* Pandas
* PyArrow
* SQLAlchemy
* Psycopg2
* Pytest
* Jupyter
* Matplotlib

## 🗄️ Data Warehouse

The warehouse follows a dimensional modeling approach.

### Fact table

`warehouse.fact_trips`

Contains trip-level information such as:

* pickup location
* dropoff location
* passenger count
* trip distance
* fare amount
* tip amount
* total amount
* payment type
* pickup datetime
* dropoff datetime

### Dimension tables

`warehouse.dim_datetime`

Contains temporal attributes:

* date
* year
* month
* day
* hour
* day of week

`warehouse.dim_location`

Contains NYC taxi location identifiers.

## ⚙️ Pipeline

The pipeline is divided into independent steps.

### 1. Load

Reads the Parquet file and loads the raw data into:

```text
raw.yellow_taxi_trips
```

Run:

```bash
python -m src.load.load_data
```

### 2. Transform

Cleans the raw data and populates the warehouse tables.

Run:

```bash
python -m src.transform.transform_data
```

### 3. Full pipeline

Runs the complete pipeline:

```bash
python -m src.pipeline
```

## 🧪 Tests

The project uses `pytest` for automated validation.

Run:

```bash
python -m pytest
```

The tests verify that:

* the raw table exists
* the fact table contains data
* the dimension tables contain data

## 📊 Analytics

Analytical queries are implemented in:

```text
src/analytics/queries.py
```

The Jupyter notebooks are dedicated to exploration, visualization, and analysis.

Database connection and ETL logic are kept outside the notebooks.

## 📝 Logging

Pipeline execution is monitored using Python's `logging` module.

Logs are:

* displayed in the terminal
* stored in `logs/pipeline.log`

Errors are captured with their traceback to facilitate debugging.

## 🔐 Configuration

Database credentials are stored in a local `.env` file.

Example:

```text
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nyc_taxi
```

The `.env` file is excluded from Git using `.gitignore`.

## 🚀 Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the project in editable mode:

```bash
python -m pip install -e .
```

Configure the `.env` file with your PostgreSQL credentials.

## 🎯 Project Goals

This project demonstrates practical Data Engineering concepts including:

* data ingestion
* ETL pipelines
* PostgreSQL
* dimensional modeling
* data cleaning
* database integration
* automated testing
* logging
* configuration management
* analytical SQL
* reproducible Python environments

## 📌 Data Source

The project uses NYC Yellow Taxi trip data provided in Parquet format.

The raw data files are intentionally excluded from the Git repository because of their size.

