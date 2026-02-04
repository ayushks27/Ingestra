Ingestra

Ingestra is an end-to-end data ingestion and processing pipeline designed to transform raw, large-scale review data into analytics-ready datasets, enabling efficient querying and visualization through a lightweight application layer.

Project Overview

    - Batch ingestion of large datasets (1+ GB) using chunked processing
    - Schema normalization and data cleaning
    - Relational data modeling using SQLite
    - Separation of ingestion, storage, and consumption layers
    - Interactive analytics via a Streamlit-based UI

The project focuses on scalability, reproducibility, and clean architecture, following real-world data engineering best practices.

Architecture

    ```mermaid
    flowchart TD
        A[Raw Data Sources<br/>(CSV / Large Files)]
        A -->|Cleaning & Normalization| B[Data Processing Scripts<br/>(Python)]
        B -->|Chunked Ingestion| C[(Relational Database<br/>SQLite)]
        C -->|Analytical Queries| D[Streamlit UI<br/>(Insights & Visualization)]

Data Model

    erDiagram
        BUSINESS {
            string b_id PK
            string name
            string postal_code
        }
    
        PREDICTED_REVIEWS {
            string business_id FK
            string Review
            float Stars
            int Authenticity_Label
        }
    
        BUSINESS ||--o{ PREDICTED_REVIEWS : has

Ingestion Workflow

    sequenceDiagram
        participant CSV as Large CSV File
        participant Script as Ingestion Script
        participant DB as SQLite Database
    
        CSV->>Script: Read chunk (200k rows)
        Script->>Script: Validate & select columns
        Script->>DB: Insert batch
        Script->>CSV: Read next chunk
        Script->>DB: Insert batch

Repository Structure

    Ingestra/
    │
    ├── Scripts/
    │   ├── setup_database.py           # Database schema creation & initialization
    │   ├── ingest_predicted_reviews.py # Chunked ingestion of large datasets
    │   ├── UI.py                       # Streamlit analytics application
    │   ├── Clean_income_zipcode_data.py
    │   └── other processing scripts
    │
    ├── data/                           # (Ignored) Raw and reference datasets
    │
    ├── notebooks/                      # Exploration & experimentation (optional)
    │
    ├── .gitignore                      # Excludes large files & generated artifacts
    ├── requirements.txt
    └── README.md

Note: Large datasets and database files are intentionally excluded from version control.

Technologies Used

    - Python (pandas, numpy, sqlite3)
    - SQLite (analytical storage)
    - Streamlit (data visualization & UI)
    - scikit-learn (text feature extraction & modeling)
    - Git (version control)

Data Model

    business(Dimension Table)
    Column	       Description
    b_id	         Unique business identifier
    name	         Business name
    postal_code	   Zip code

    predicted_reviews (Fact Table)
    Column	              Description
    business_id	          Foreign key to business table
    Review	              Review text
    Stars	                Rating score
    True(1)/Deceptive(0)	Review authenticity label

Setup & Installation

Clone the repository

    git clone https://github.com/<your-username>/ingestra.git
    cd ingestra

Create and activate environment

    conda create -n ingestra python=3.10
    conda activate ingestra
    pip install -r requirements.txt

Data Ingestion Workflow

    Step 1: Initialize the database
    Creates schema and loads business metadata.
    python Scripts/setup_database.py

    Step 2: Ingest large review dataset
    Processes large CSV files using chunked ingestion to avoid memory issues.
    python Scripts/ingest_predicted_reviews.py

This script is designed to handle datasets >1 GB efficiently.

Run the Application

Launch the Streamlit UI: 

    streamlit run Scripts/UI.py

Then open:

    http://localhost:8501

UI Features

    - Input business name and zipcode
    - Compute fake review ratio
    - Analyze key phrases influencing ratings
    - Visualize insights interactively

Key Engineering Decisions

    - Chunked ingestion to handle large datasets safely
    - Schema normalization before loading into the database
    - Database-backed querying instead of loading raw files in the UI
    - Separation of concerns between ingestion, storage, and visualization

Reproducible pipelines over committing raw data

What This Project Demonstrates

    - Real-world data ingestion patterns
    - Handling of large datasets with limited memory
    - Clean relational modeling for analytics
    - Transition from notebooks to production scripts
    - End-to-end ownership of a data pipeline

Future Improvements

    - Replace SQLite with PostgreSQL / Redshift
    - Add data quality checks & logging
    - Introduce orchestration (Airflow)
    - Add automated tests for ingestion scripts
    - Support cloud storage (S3-style ingestion)

Deployment

    - The Streamlit application is deployed using a lightweight demo database for visualization.
    - Large-scale ingestion and full datasets are intentionally excluded from deployment and are handled via local or cloud-based ingestion pipelines.


Author

    Purnendu Raghav Srivastava
    Data Engineering & Analytics Enthusiast
