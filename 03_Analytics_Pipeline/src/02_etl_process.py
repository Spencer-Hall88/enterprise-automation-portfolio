import sqlite3
import pandas as pd

def run_etl_pipeline():
    """Extracts data from SQLite, transforms it using Pandas, and loads it to CSV."""
    print("Step 1: Extracting data from SQLite database...")
    conn = sqlite3.connect('../data/analytics_practice.db')
    
    # We use SQLite's julianday() function to calculate date differences in days, then multiply by 24 for hours.
    sql_query = """
    SELECT 
        ticket_id,
        created_date,
        resolved_date,
        customer_tier,
        agent_id,
        (julianday(resolved_date) - julianday(created_date)) * 24 AS resolution_hours
    FROM raw_tickets
    """
    
    # Read directly into a Pandas DataFrame
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    
    print("Step 2: Performing Data Transformation...")
    # Clean customer tier text (strip whitespace, convert to uppercase)
    df['customer_tier'] = df['customer_tier'].str.strip().str.upper()
    
    # Handle Nulls: Tag unresolved tickets
    df['resolution_hours'] = df['resolution_hours'].fillna(-1)
    df['is_resolved'] = df['resolved_date'].notnull()
    
    # Multi-Tier SLA Logic: VIP <= 24 hours, STANDARD <= 48 hours (1=Yes, 0=No)
    def check_sla(row):
        # If the ticket isn't resolved yet, it's not SLA compliant
        if row['resolution_hours'] < 0:
            return 0
            
        if row['customer_tier'] == 'VIP' and row['resolution_hours'] <= 24:
            return 1
        elif row['customer_tier'] == 'STANDARD' and row['resolution_hours'] <= 48:
            return 1
        else:
            return 0
            
    df['sla_compliant'] = df.apply(check_sla, axis=1)

    print("Step 3: Loading transformed data to CSV...")
    # Export clean dataset for dashboard ingestion
    output_path = '../data/kpi_summary.csv'
    df.to_csv(output_path, index=False)
    print(f"ETL pipeline complete. Clean dataset exported to {output_path}")

if __name__ == "__main__":
    run_etl_pipeline()