# Standard Operating Procedure: Lightweight Asset Tracker Deployment

## Document Purpose
This runbook details the local execution and environment setup for the Fleet Maintenance Tracker application. It outlines the steps required to initialize the local server, run the Streamlit frontend, and interact with the SQLite backend.

## Phase 1: Environment Setup

**1. Directory Initialization**
Ensure your local environment is structured under the `04_Lightweight_Asset_Tracker` root directory.

**2. Python Dependencies**
Ensure the host machine is running Python 3.8+ and install the required web framework and data handling libraries.
* Command: `pip install streamlit pandas`
* Note: `sqlite3` is a built-in Python library and requires no separate installation.

## Phase 2: Application Execution

**1. Initialize the Server**
Navigate to the root directory containing the application file (`app.py`). Execute the Streamlit run command to compile the Python script into a local web server.
* Command: `streamlit run app.py`

**2. Database Initialization (Auto-Execute)**
Upon the first run, the `init_db()` function will automatically execute, scanning for `fleet_data.db`. If the database does not exist, the SQLite engine will generate it locally and establish the `maintenance_logs` relational schema.

## Phase 3: UI Interaction & Testing

**1. Data Ingestion (Write)**
* Navigate to the **"Log a Maintenance Issue"** tab in your browser.
* Fill out the structured form. 
* Clicking 'Submit' triggers the `add_log()` function, mapping the form inputs to a SQL `INSERT INTO` statement and committing the transaction to the database.

**2. Data Validation (Read)**
* Navigate to the **"View Active Issues"** tab.
* The UI will trigger a SQL `SELECT` query, retrieve all 'Open' tickets, sort them by urgency using Pandas logic, and render the resulting dataframe directly into the browser.
