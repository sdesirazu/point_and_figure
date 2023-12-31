import math
import time
import gspread
import json
import os
import sys
from google.oauth2 import service_account
from datetime import datetime as dt, date, time, timedelta
import yfinance as yf
import upload_basic
import calcpnf
from pytz import timezone
from BSMerton import BSMerton
import last_div_value
import rfr

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

sheet = file.open("Weekly Options - Easy Income")

sheet = sheet.worksheet("Weekly Options List") #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet


column_number = 1
col = sheet.col_values(column_number)
col = col[6:]
start = 7
row_number = start
init_row_number = row_number

grid = []
today = dt.now()
today_string = today.strftime("%Y-%m-%d %H:%M:%S")
friday = today + timedelta( (4-today.weekday()) % 7 )
dt_string = friday.strftime("%Y-%m-%d")
percent = sheet.acell('F1').value
percent = float(percent)

for ticker in col:
    if ticker == "Ticker":
        continue
    if ticker == "Filter":
        continue
    li = []
    try:
        data = yf.Ticker(ticker)
        price = data.info['currentPrice']

        price = price + (price * (percent / 100.0))
        opt = data.option_chain(dt_string)
        df = opt.calls

        price=float(price)
        df_sorted = df.sort_values(by='strike',ascending=True)
        df_closest = (df_sorted[df_sorted["strike"]>=price])
        closest_value = df_closest["strike"].tolist()[0]
        impliedVolatility = df_closest["impliedVolatility"].tolist()[0]

        li.append(calcpnf.calcpnf(ticker,startDate))
        li.append(price)
        li.append(ticker)
        li.append(closest_value)

        bid = df_closest["bid"].tolist()[0]
        if(math.isnan(bid)):
            bid = 0.0
        li.append(bid)

        ask = df_closest["ask"].tolist()[0]
        if(math.isnan(ask)):
            ask = 0.0
        li.append(ask)

        lastPrice = df_closest["lastPrice"].tolist()[0]
        if(math.isnan(lastPrice)):
            lastPrice = 0.0
        li.append(lastPrice)
        
        openInterest = df_closest["openInterest"].tolist()[0]
        if(math.isnan(openInterest)):
            openInterest = 0.0
        li.append(openInterest)

        # calculate delta
        last_dividend = last_div_value.last_div_value(data)
        risk_free_rate = rfr.get_rfr()
        dividend_continuous_rate = last_dividend/data.info['currentPrice']
        num_days_to_expire = friday - today
        
        test = BSMerton([1,data.info['currentPrice'],closest_value,risk_free_rate,dividend_continuous_rate,num_days_to_expire.days,impliedVolatility])

        li.append(test.delta()[0])

    except:
        print("Failed on ticker "+ticker)

    row_number = row_number + 1

    grid.append(li)
        
location = "O"+str(init_row_number)+":W"+str(row_number)+""

now_time = dt.now(timezone('Australia/Sydney'))
fmt = "%Y-%m-%d %H:%M:%S %Z%z"
now_time = now_time.strftime(fmt)

sheet.update('B3', now_time)
sheet.batch_update([{
    'range': location,
    'values': grid,
}])
