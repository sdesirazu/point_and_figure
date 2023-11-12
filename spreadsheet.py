import gspread
import json
import os
import sys
from google.oauth2 import service_account
from point_and_figure import PointAndFigure 

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

sheet = file.open("pnf") #open sheet

print("desirazu")

sheet = sheet.sheet1 #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet

col = sheet.col_values(1)

column_number = 1
row_number = 1
for cell in col:
    ticker = cell
    model = PointAndFigure(step, ticker, startDate)
    print("model is "+model)
    write_column_number = column_number + 1
    sheet.update_cell(row_number, write_column_number, model)
    row_number = row_number + 1

