import yfinance as yf
import duckdb
import pandas as pd
from datetime import datetime

# Fetch AAPL data
ticker = "AAPL"
df = yf.download(ticker, period="1y", interval="1d")
df.reset_index(inplace=True)

# Save into DuckDB
conn = duckdb.connect("stocks.duckdb")
conn.execute("CREATE TABLE IF NOT EXISTS stock_data AS SELECT * FROM df")
conn.execute("INSERT INTO stock_data SELECT * FROM df")

# Example query
result = conn.execute("SELECT Date, Close FROM stock_data LIMIT 5").fetchdf()
print(result)

# Add a quick signal
df["MA50"] = df["Close"].rolling(50).mean()
df["MA200"] = df["Close"].rolling(200).mean()
latest = df.iloc[-1]
if latest["MA50"] > latest["MA200"]:
    print("📈 BUY signal for", ticker)
else:
    print("📉 No Buy signal yet")
