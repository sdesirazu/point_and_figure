import yfinance as yf
import pandas as pd
import math
import mplfinance as mpf

instrument = yf.Ticker("MSFT")
startDate = "2023-01-01"
endDate = None

#hist = instrument.history(start=startDate, end=endDate)
#df = pd.DataFrame({'Date':hist['Close'].index, 'Open': hist['Open'].values, 'High': hist['High'].values, 'Low': hist['Low'].values, 'Close': hist['Close'].values, 'Volume': hist['Volume'].values})

df = yf.download("MSFT", period='1mo')
print(df)
cv = {}
mpf.plot(df,type='pnf',return_calculated_values=cv)

print("srinvias")
print(cv.keys())
print("desirazu")
