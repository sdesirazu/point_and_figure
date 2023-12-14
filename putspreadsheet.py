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


puts_strike_guide = sheet.col_values(4)

column_number = 1
col = sheet.col_values(column_number)
col = col[5:]
start = 6
row_number = start
init_row_number = row_number

grid = []
for ticker in col:
    if ticker == "Ticker":
        continue
    li = []
    try:
        data = yf.Ticker(ticker)
        price = puts_strike_guide[row_number]
        today = dt.now()
        friday = today + timedelta( (4-today.weekday()) % 7 )
        dt_string = friday.strftime("%Y-%m-%d")

        opt = data.option_chain(dt_string)

        # Puts
        df = opt.puts
        price=float(price)
        df_closest = df.iloc[(df["strike"]-price).abs().argsort()[:1]]
        closest_value = df_closest["strike"].tolist()[0]
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
        li.append(price)

    except:
        print("Failed on ticker "+ticker)
    row_number = row_number + 1
    grid.append(li)
        
location = "E"+str(init_row_number)+":K"+str(row_number)+""

sheet.batch_update([{
    'range': location,
    'values': grid,
}])
