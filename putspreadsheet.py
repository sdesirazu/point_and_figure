from pytz import timezone
import pandas as pd
import math
import time
import gspread
import json
import os
import sys
from google.oauth2 import service_account
from datetime import datetime as dt, date, time, timedelta
import yfinance as yf
from BSMerton import BSMerton
import last_div_value
import rfr
import calcpnf
import numpy as np
from pyfinviz.quote import Quote
from finvizfinance.earnings import Earnings

my_columns = ['currentPrice','strike','ticker','bid','ask','lastPrice','openInterest','delta']

def earnings(ticker):
  for key in earnings_partition_days.keys():
    mask = earnings_partition_days[key]['Ticker'].str.fullmatch(ticker)
    if(mask.any()):
      return ("Yes")
  return ("No")

  
def rsi(ticker):
    quote = Quote(ticker=ticker)
    # available variables:
    if(not quote.exists):
      return 0.0
    return(quote.fundamental_df["RSI (14)"])
  
def find_10_delta_row(optionType, ticker,data,dt_string,friday,today):
    grid = []
    try:
        price = data.info['currentPrice']
        
        opt = data.option_chain(dt_string)
        
        # Puts or calls
        if(optionType == -1):
            df = opt.puts

        if(optionType == 1):
            df = opt.calls
            
        if(df.size == 0):
            my_df = pd.DataFrame(data=grid,columns=my_columns)
            return my_df

        df_sorted = df.sort_values(by='strike',ascending=False)

        currentPrice = float(price)
        for index, row in df_sorted.iterrows():
            li = []
            strike = row['strike']
            bid = row['bid']
            ask = row['ask']
            lastPrice = row['lastPrice']
            openInterest = row['openInterest']
            impliedVolatility = row['impliedVolatility']

            # do not do if this number is 0.0
            if (impliedVolatility) < 0.001:
                continue

            last_dividend = last_div_value.last_div_value(data)
            dividend_continuous_rate = last_dividend/data.info['currentPrice']
            num_days_to_expire = friday - today
        
            test = BSMerton([optionType,currentPrice,strike,risk_free_rate,dividend_continuous_rate,num_days_to_expire.days,impliedVolatility])
            li.append(float(currentPrice))
            li.append(float(strike))
            li.append(ticker)
            li.append(float(bid))
            li.append(float(ask))
            li.append(float(lastPrice))
            li.append(float(openInterest))
            li.append(float(test.delta()[0]))
            grid.append(li)
        # create the dataframe
        my_df = pd.DataFrame(data=grid,columns=my_columns)
        if(optionType == -1):
            df_closest = my_df[my_df["delta"]>= -0.15]
        if(optionType == 1):
           df_closest = my_df[my_df["delta"]>= 0.10]
        return df_closest

    except Exception as e: print("Exception is ", e)




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

sheet = sheet.worksheet("Weekly Options List-OLD") #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

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
risk_free_rate = rfr.get_rfr()

# get the earnings once from finviz
earnings_df = Earnings(period='Next Week')
earnings_partition_days = earnings_df.partition_days()


for ticker in col:
    if ticker == "Ticker":
        continue
    if ticker == "Filter":
        continue
    
    li = []
    grid.append(li)    
    row_number = row_number + 1
    
    try:
        data = yf.Ticker(ticker)
        xoro = calcpnf.calcpnf(data,ticker,startDate)
        if(xoro == 'X'):
            optionType = -1
        if(xoro == 'O'):
            optionType = 1
        if(xoro == 'U'):
            li.append(0.0)
            li.append(0.0)
            li.append(ticker)
            li.append(0.0)
            li.append(0.0)
            li.append(0.0)
            li.append(0.0)
            li.append(0.0)            
            li.append(0.0)
            li.append("U")
            li.append(0.0)
            li.append("Unknown")
            continue

        row = find_10_delta_row(optionType,ticker,data,dt_string,friday,today)
        if(row.size ==0):
            li.append(0.0)
            li.append(0.0)
            li.append(ticker)
            li.append(0.0)
            li.append(0.0)
            li.append(0.0)
            li.append(0.0)
            li.append(0.0)            
            li.append(0.0)
            li.append("U")
            li.append(0.0)
            li.append("Unknown")
            continue
        
        row = row.iloc[0]
        
        li.append(float(row['currentPrice']))

        li.append(float(row['strike']))

        li.append(ticker)

        li.append(float(row['strike']))

        bid = float(row['bid'])

        if(math.isnan(bid)):
            bid = 0.0

        li.append(bid)

        ask = float(row['ask'])

        if(math.isnan(ask)):
            ask = 0.0

        li.append(ask)

        lastPrice = float(row['lastPrice'])

        if(math.isnan(lastPrice)):
            lastPrice = 0.0

        li.append(lastPrice)

        openInterest = float(row['openInterest'])

        if(math.isnan(openInterest)):
            openInterest = 0.0

        li.append(openInterest)

        delta = float(row['delta'])

        if(math.isnan(delta)):
            delta = 0.0
            
        li.append(delta)

        li.append(xoro)
        
        li.append(float(rsi(ticker).iloc[0]))
      
        li.append(earnings(ticker))

    except Exception as e: 
        print("Failed on ticker ", ticker, " ", e)
        li.append(0.0)
        li.append(0.0)
        li.append(ticker)
        li.append(0.0)
        li.append(0.0)
        li.append(0.0)
        li.append(0.0)
        li.append(0.0)            
        li.append(0.0)
        li.append("U")
        li.append(0.0)
        li.append("Unknown")
        
location = "E"+str(init_row_number)+":P"+str(row_number)+""

sheet.batch_update([{
    'range': location,
    'values': grid,
}])

now_time = dt.now(timezone('Australia/Sydney'))
fmt = "%Y-%m-%d %H:%M:%S %Z%z"
now_time = now_time.strftime(fmt)
sheet.update_cell(3,2,now_time)
