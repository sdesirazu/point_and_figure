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
sheet = sheet.'stock list' #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet

col = sheet.col_values(1)

column_number = 2
row_number = 4
for cell in col:
    ticker = cell
    print(ticker)
    try:
        model = PointAndFigure(step, ticker, 0, startDate)
        xoro = model.chart()
        print("model is "+xoro)
        write_column_number = column_number + 1
        sheet.update_cell(row_number, write_column_number, xoro)

        # datetime object containing current date and time
        now = datetime.now()
        sheet.update_cell(row_number, write_column_number+1, now.strftime("%c"))
        row_number = row_number + 1
        time.sleep(2)
    except:
        print("Failed on ticker")

