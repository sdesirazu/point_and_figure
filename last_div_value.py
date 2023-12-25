import math
import time
import gspread
import json
import os
import sys
from datetime import datetime as dt, date, time, timedelta


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

