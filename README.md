# analyze_managers

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A data analysis project for evaluating manager performance in chat communications. This project calculates response times of managers in a chat system.

## Dashboard

<a target="_blank" href="https://datalens.yandex/2ord135cfkr4o">DataLens Dashboard</a>

## Features

- Calculates average response times for managers
- Dual implementation (SQL and Python) for performance comparison
- Handles working hours logic (9:30-24:00)
- Accounts for non-working hours in calculations
- Removes consecutive duplicate messages for accurate analysis

## Project Organization

```
├── Makefile         <- Makefile with convenience commands like `make requirements` or `make format`
├── README.md        <- The top-level README for developers using this project.
├── data
│   ├── external     <- Data from third party sources.
│   ├── interim      <- Intermediate data that has been transformed.
│   ├── processed    <- The final, canonical data sets for modeling.
│   └── raw          <- The original, immutable data dump.
│
├── notebooks        <- Jupyter notebooks. Naming convention is a number (for ordering), the creator's initials, and a short `-` delimited description.
|    └── reports      <- Reports
│         └── 0.1-alena-calculate_managers_response_times.ipynb       <- Calculate managers response times using python
│         └── 0.2-alena-calculate_managers_response_times_sql.ipynb   <- Calculate managers response times using SQL
│
├── pyproject.toml   <- Project configuration file
│
├── requirements.txt <- The requirements file for reproducing the analysis environment
│
├── setup.cfg        <- Configuration file for flake8
│
└── analyze_managers <- Source code for use in this project.
    │
    ├── calculate      <- Scripts to download or generate data
    │   └── calculate_response_times.py   <- Calculate response times using python
    │   └── calculate_response_times.sql  <- Calculate response times using SQL
    ├── data           <- Scripts to download or generate data
    │   └── db.py                <- Database connection
    │   └── make_dataset.py      <- Make dataset
    │   └── prepare_dataset.py   <- Prepare dataset
    ├── util           <- Scripts to download or generate data
    │   └── date_time_util.py    <- Date time utils
    └── config.py      <- Store useful variables and configuration
```

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
make create_environment
# or
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
make requirements
# or
pip install -r requirements.txt
```

## Usage

### Running Analysis

You can analyze manager response times using either SQL or Python implementation:

1. Using SQL:
```python
from analyze_managers.data.db import Database
import pandas as pd

with Database() as db:
    connection = db.get_connection()
    sql_average_response_times = pd.read_sql_query('path/to/sql_query.sql', connection)
```

2. Using Python:
```python
from analyze_managers.data.make_dataset import get_chat_messages, get_managers
from analyze_managers.data.db import Database
from analyze_managers.data.prepere_dataset import prepare_chat_messages
from analyze_managers.calculate.calculate_response_times import calculate_response_times, calculate_average_response_times

database = Database()

with database as db:
  connection = db.get_connection()
  chat_messages = get_chat_messages(connection)
  managers = get_managers(connection)

prepared_chat_messages = prepare_chat_messages(chat_messages)
response_times = calculate_response_times(prepared_chat_messages)
average_response_times = calculate_average_response_times(response_times, managers)
```

### Development Tools

- **Black** - code formatter: `black {source_file_or_directory}...`
- **Jupyter notebook**: `jupyter notebook notebooks`
- **Flake8** - code linter: `flake8 path/to/code/`
- **isort** - import sorter: `isort .`

## Environment Variables

The project uses environment variables for configuration. Create a `.env` file with:

```
DATABASE_HOST=your_host
DATABASE_NAME=your_database
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_PORT=your_port
```
