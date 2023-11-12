import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import sys

try:
    startDate = sys.argv[1]
except:
    print("invalid or missing start date")
    
try:
    step = float(sys.argv[2])
except:
    print("invalid or missing step value")


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
sheet = file.open("pnf") #open sheet
sheet = sheet.Sheet1 #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

# for each cell in the sheet call the point and figure and write it back to the sheet

col = sheet.col_values(1)
print(col)

for cell in col:
    print(cell.value)
    ticker = cell.value
    model = PointAndFigure(step, ticker, startDate)
    row_number = cell.row
    column_number = cell.col
    write_column_number = column_number + 1
    sheet.update_cell(row_number, write_column_number, $model)

