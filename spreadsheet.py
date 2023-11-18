import time
import gspread
import json
import os
import sys
from google.oauth2 import service_account
from point_and_figure import PointAndFigure 
from datetime import datetime

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

print("srinivas")

file = gspread.authorize(scoped_credentials) # authenticate the JSON key with gspread

#####sheet = file.open("pnf") #open sheet
sheet = file.open("231113-Wkly Options")
print("desirazu")

#sheet = sheet.sheet1 #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
sheet = sheet.worksheet("P&F") #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet

column_number = 2
col = sheet.col_values(column_number)

start = 1
row_number = 4
init_row_number = row_number
grid = []
for ticker in col:
    # start with column 4
    if start < row_number:
        start = start + 1
        continue
    print(ticker)
    try:
        li = []
        model = PointAndFigure(step, ticker, 0, startDate)
        xoro = model.chart()
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        li.append(ticker)
        li.append(xoro)
        li.append(dt_string)
        grid.append(li)
        row_number = row_number + 1
    except:
        print("Failed on ticker")

        
location = "'K"+str(init_row_number)+":M"+str(row_number)+"'"
print(location)
print(grid)
sheet.batch_update([{
    'range': location,
    'values': grid,
}])
    
