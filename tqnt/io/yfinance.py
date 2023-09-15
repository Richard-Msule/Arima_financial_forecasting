import yfinance as yf

def download_dataframes(tickers, filename, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    data.to_csv(filename)
    return data


### 

