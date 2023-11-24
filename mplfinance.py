import yfinance as yf
import pandas as pd
import math
import mplfinance as mpf

instrument = yf.Ticker("MSFT")

hist = instrument.history(start=self.startDate, end=self.endDate)
df = pd.DataFrame({'Date':hist['Close'].index, 'Close': hist['Close'].values})


close_prices = df['Close']
dates = df['Date']

print(close_prices)
print(dates)

