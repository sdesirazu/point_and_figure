import yfinance as yf
from pypnf import PointFigureChart

symbol = 'AAPL'

data = yf.Ticker(symbol)
ts = data.history(start='2018-01-01', end='2018-06-30')

# reset index
ts.reset_index(level=0, inplace=True)

# convert pd.timestamp to string
ts['Date'] = ts['Date'].dt.strftime('%Y-%m-%d')

# select required keys
ts = ts[['Date','Open','High','Low','Close']]

# convert DataFrame to dictionary
ts = ts.to_dict('list')


pnf = PointFigureChart(ts=ts, method='cl', reversal=3, boxsize=2, scaling='abs', title='AAPL')
pnf.get_trendlines()
print(pnf)
