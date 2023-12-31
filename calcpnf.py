import yfinance as yf
from pypnf import PointFigureChart


def calcpnf(data,ticker,startDate):
    # function body 

    try:
        price = data.info['currentPrice']

        if price < 0.25:
            box = 0.0625
        elif price >= 0.25 and price < 1.00:
            box = 0.125
        elif price >= 1.00 and price < 5.00:
            box = 0.25
        elif price >= 5.00 and price < 20.00:
            box = 0.50
        elif price >= 20.00 and price < 100:
            box = 1.00
        elif price >= 100 and price < 200:
            box = 2.00
        elif price >= 200 and price < 500:
            box = 4.00
        elif price >= 500 and price < 1000:
            box = 5.00
        elif price >= 1000 and price < 2500:
            box = 10.00
        elif price >= 2500 and price < 25000:
            box = 50.00
        else:
            box = 500.00

        ts = data.history(start=startDate, end=None)
        
        # reset index
        ts.reset_index(level=0, inplace=True)
        
        # convert pd.timestamp to string
        ts['Date'] = ts['Date'].dt.strftime('%Y-%m-%d')
        
        # select required keys
        ts = ts[['Date','Open','High','Low','Close']]
    
        # convert DataFrame to dictionary
        ts = ts.to_dict('list')
        
        pnf = PointFigureChart(ts=ts, method='h/l', reversal=3, boxsize=box, scaling='abs', title=ticker)
        y = pnf.matrix.shape[1] - 1
        for x in pnf.matrix:
            if x[y] == 1 or x[y] == -1:
                if x[y] == 1:
                    xoro = 'X'
                else:
                    xoro = 'O'
                return xoro
    except:
        print("Failed on ticker "+ticker)

    return "U"
