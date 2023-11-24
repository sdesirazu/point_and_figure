import yfinance as yf
import pandas as pd
import math
import mplfinance as mpf

instrument = yf.Ticker("MSFT")
startDate = "2023-01-01"
endDate = None

hist = instrument.history(start=startDate, end=endDate)
df = pd.DataFrame({'Date':hist['Date'].index, 'Open': hist['Open'].values, 'High': hist['High'].values, 'Low': hist['Low'].values, 'Close': hist['Close'].values, 'Volume': hist['Volume'].values})
df = df.set_index('Date')
close_prices = df['Close']
dates = df['Date']

print(close_prices)
print(dates)

cv = {}
mpf.plot(df,type='pnf',return_calculated_values=cv)

print("srinvias")
print(cv['pnf_counts'])
print(cv['pnf_values'])
print("desirazu")
