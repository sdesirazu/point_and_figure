import time
import gspread
import json
import os
import sys
from google.oauth2 import service_account
from datetime import datetime
import yfinance as yf
from pypnf import PointFigureChart

try:
    step = float(sys.argv[1])
except:
    print("invalid or missing step value")


try:
    startDate = sys.argv[2]
except:
    print("invalid or missing start date")
    

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

TOKEN = os.environ['TOKEN']

service_account_info = json.loads(TOKEN)
credentials = service_account.Credentials.from_service_account_info(
    service_account_info)

scoped_credentials = credentials.with_scopes(scopes)


file = gspread.authorize(scoped_credentials) # authenticate the JSON key with gspread

sheet = file.open("P&F")

sheet = sheet.worksheet("P&F") #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet

column_number = 2
col = sheet.col_values(column_number)
start = 2
row_number = start
init_row_number = row_number

grid = []
for ticker in col:
    if ticker == "Ticker":
        continue
    li = []
    li.append(ticker)
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    li.append(dt_string)
    try:
        data = yf.Ticker(ticker)
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
        pnf.save("download.jpeg")
        upload_basic(scoped_credentials)
        y = pnf.matrix.shape[1] - 1
        for x in pnf.matrix:
            if x[y] == 1 or x[y] == -1:
                if x[y] == 1:
                    xoro = 'X'
                else:
                    xoro = 'O'
                li.append(xoro)
                break
    except:
        print("Failed on ticker"+ticker)

    row_number = row_number + 1
    grid.append(li)
        
location = "K"+str(init_row_number)+":M"+str(row_number)+""
    
sheet.batch_update([{
    'range': location,
    'values': grid,
}])
