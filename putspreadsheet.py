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
import BSMerton

def last_div_value(data):
    dividends = data.dividends
    div_sorted = dividends.sort_values(ascending=False)
    last_div = 0.0
    now = dt.now()
    curr_year = now.year
    for k in div_sorted.keys():
        last_div_date = k
        if curr_year == last_div_date.year or (curr_year - 1) == (last_div_date.year):
            last_div = (div_sorted[k])
            break
    return (last_div)

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
        li.append(price)

        price = price - (price * (percent / 100.0))

        opt = data.option_chain(dt_string)

        # Puts
        df = opt.puts

        price=float(price)
        df_sorted = df.sort_values(by='strike',ascending=False)
        df_closest = (df_sorted[df_sorted["strike"]<=price])
        closest_value = df_closest["strike"].tolist()[0]
        impliedVolatility = df_closest["impliedVolatility"].tolist()[0]

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

        last_dividend = last_div_value(data)
        risk_free_rate = 0.06
        dividend_continuos_rate = last_dividend/data.info['currentPrice']
        num_days_to_expire = friday - today
        
        test = BSMerton([-1,data.info['currentPrice'],closest_value,risk_free_rate,dividend_continuous_rate,num_days_to_expire.days,impliedVolatility])

        print('Premium: {}\nDelta:   {}\nVega:    {}'.format(test.premium()[0],test.delta()[0], test.vega()[0]))
        print('Theta:   {}\nRho:     {}\nPhi:     {}'.format(test.theta()[0],test.rho()[0], test.phi()[0]))
        print('Gamma:   {}\nCharm:   {}\nVanna:   {}'.format(test.gamma()[0],test.dDeltadTime()[0], test.dDeltadVol()[0]))
        print('Vomma:   {}'.format(test.dVegadVol()[0]))

    except:
        print("Failed on ticker "+ticker)
    row_number = row_number + 1
    grid.append(li)
        
location = "E"+str(init_row_number)+":L"+str(row_number)+""

sheet.batch_update([{
    'range': location,
    'values': grid,
}])
