import pandas as pd
import pymysql
from sqlalchemy import create_engine

# Read CSV file into a DataFrame
csv_file_path = '/Users/tiagomiguelrebelomirotes/Desktop/aml_system/HI-Small_Trans.csv'
df = pd.read_csv(csv_file_path)

df.rename(columns={
    'Timestamp': 'timestamp',
    'From Bank': 'from_bank',
    'Account': 'from_account',
    'To Bank': 'to_bank',
    'Account.1': 'to_account',
    'Amount Received': 'amount_received',
    'Receiving Currency': 'receiving_currency',
    'Amount Paid': 'amount_paid',
    'Payment Currency': 'payment_currency',
    'Payment Format': 'payment_format',
    'Is Laundering': 'is_laundering'
}, inplace=True)

# Convert 'Timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Ensure 'Is Laundering' is a boolean
df['is_laundering'] = df['is_laundering'].astype(bool)

# Database connection
engine = create_engine('mysql+pymysql://root:Banana22!@localhost/aml_system')

# Insert data into transactions table
df.to_sql('transactions', con=engine, if_exists='append', index=False)
print("Data imported successfully!")


