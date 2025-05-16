import pandas as pd
import os
import logging

def fetch_market_data():
    """Read market data directly from the CSV file"""
    csv_path = 'popular_stocks_data.csv'
    
    try:
        # Check if CSV file exists
        if not os.path.exists(csv_path):
            logging.error(f"CSV file not found: {csv_path}")
            return []
        
        # Read the CSV file
        df = pd.read_csv(csv_path)
        
        # Convert DataFrame to list of dictionaries
        market_data = df.to_dict('records')
        
        return market_data
        
    except Exception as e:
        logging.error(f"Error reading market data from CSV: {str(e)}")
        return []