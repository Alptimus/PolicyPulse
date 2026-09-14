# import yfinance as yf

# # Download NIFTY 50 historical data
# nifty_50 = yf.download("^NSEI", start="2012-02-13", end="2025-12-05")

# print(nifty_50.head())
# print(nifty_50.tail())

import pandas as pd
import numpy as np
import yfinance as yf

# ---------------------------------------------------------
# STEP 1: Clean and reshape the RBI data
# ---------------------------------------------------------
# Assuming your CSV is named 'rbi_rates.csv'

filename = 'data/rbi_rates.csv'

rbi_df = pd.read_csv(filename)

# 1. Convert the 'Effective Date' to a proper datetime object (Format: DD-MM-YYYY)
rbi_df['Effective Date'] = pd.to_datetime(rbi_df['Effective Date'], format='%d-%m-%Y')

# print(rbi_df.head())


# 2. Filter to just the Date and Repo Rate, then sort chronologically
rbi_repo = rbi_df[['Effective Date', 'Repo']].copy()
rbi_repo.sort_values('Effective Date', inplace=True)
rbi_repo.set_index('Effective Date', inplace=True)

# 3. Resample to a monthly frequency. 
# Since rates change on specific days, we forward-fill (ffill) so every month 
# reflects the active rate at the end of that month.
rbi_monthly = rbi_repo.resample('ME').ffill() 
rbi_monthly.dropna(subset=['Repo'], inplace=True)

# Convert index to a Year-Month period to make merging cleaner later
rbi_monthly.index = rbi_monthly.index.to_period('M')

# print(rbi_monthly.head())
# exit()  # Remove this line after verifying the data


# ---------------------------------------------------------
# STEP 2: Clean the yfinance data
# ---------------------------------------------------------
# 1. Pull daily OHLC for ^NSEI
nifty_50 = yf.download("^NSEI", start="2012-02-13", end="2025-12-05")

# print(nifty_50.head())
# exit()  # Remove this line after verifying the data

# Handle the MultiIndex column structure returned by recent yfinance versions
if isinstance(nifty_50.columns, pd.MultiIndex):
    close_prices = nifty_50['Close']['^NSEI']
else:
    close_prices = nifty_50['Close']

nifty_df = pd.DataFrame({'Close': close_prices})

# 2. Compute daily log returns
nifty_df['Log_Return'] = np.log(nifty_df['Close'] / nifty_df['Close'].shift(1))

# 3. Resample to monthly: compute realized volatility and monthly average price
monthly_nifty = nifty_df.resample('ME').agg(
    Monthly_Avg_Close=('Close', 'mean'),
    Volatility=('Log_Return', lambda x: x.std() * np.sqrt(21)) # std dev * sqrt(21 trading days)
)

# Convert index to Year-Month period for merging
monthly_nifty.index = monthly_nifty.index.to_period('M')


# ---------------------------------------------------------
# STEP 3: Merge on date
# ---------------------------------------------------------
# Join RBI monthly repo rate with the monthly volatility/price table
master_df = pd.merge(monthly_nifty, rbi_monthly, left_index=True, right_index=True, how='inner')

# Convert the period index back to standard timestamps for easier plotting/exporting
master_df.index = master_df.index.to_timestamp()

print(master_df.head())

with open('data/master_data.csv', 'w') as f:
    master_df.to_csv(f, index=True)

print(f"\nTotal rows in master table: {len(master_df)}")