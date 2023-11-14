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
sheet = sheet.worksheet("Stock List") #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet

column_number = 2
col = sheet.col_values(column_number)

height = 3
width = 1000
grid = [[' ' for _ in range(width)] for _ in range(height)]

start = 1
init_row_number = 4
init_row_number = row_number
for ticker in col:
    # start with column 4
    if start < row_number:
        start = start + 1
        continue
    print(ticker)
    try:
        model = PointAndFigure(step, ticker, 0, startDate)
        xoro = model.chart()
        # datetime object containing current date and time
        now = datetime.now()

        grid[row_number][0] = ticker
        grid[row_number][1] = xoro
        grid[row_number][2] = now
        row_number = row_number + 1
        time.sleep(2)
    except:
        print("Failed on ticker")

        
    location = "'C"+init_row_number+":D"+row_number+"'"
    print(location)
    sheet.update_cell(location, grid)
    
