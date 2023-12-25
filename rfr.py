import yfinance as yf
def get_rfr():
    # risk free rate

    rfr = yf.Ticker("^IRX")

    rfr = rfr.info["fiftyDayAverage"])/100.0

    return rfr
