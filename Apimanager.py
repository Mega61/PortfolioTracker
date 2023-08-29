import requests
import pandas as pd
from datetime import date
from time import sleep


fileExist = True
try:
    df = pd.read_csv("StockIndex.csv")    
except:
    fileExist = False
    print('Warning!: CSV File does not exists')

if fileExist is False:
    df = pd.DataFrame(columns=['date','total_balance', 'portfolio_quantity', 'portfolio_price' ,'daily_change','acc_change','deposit','total_deposits','profit'])

today_date = date.today()
today_day = today_date.day
monthly_deposit = 255
apiKey = 'TYN58ZBCTHT1ZLK3'
tickers = ["VOO", "VTI", "VTIP", "VGSH", "BRK.B", "ICLN"]
portfolio = {}
dummy = False
dummyDict = {'VOO': 412.6400, 'VTI': 223.1900, 'VTIP': 47.3400, 'VGSH': 57.7500, 'BRK.B': 358.2900, 'ICLN': 16.5400}
if dummy == False:
    for ticker in tickers:
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + \
            ticker + '&apikey=' + apiKey
        r = requests.get(url)
        sleep(13)
        data = r.json()
        portfolio[ticker] = float(data['Global Quote']['05. price'])
else:
    portfolio = dummyDict

print(portfolio)
proportions = {"VOO": 0.3, "VTI": 0.2, "VTIP": 0.1,
               "VGSH": 0.3, "BRK.B": 0.05, "ICLN": 0.05}
portfolio_price = 0

for ticker in tickers:
    print(proportions[ticker])
    p = portfolio[ticker]
    portfolio_price = portfolio_price + p * proportions[ticker]

if fileExist:
    day_before_row = df.iloc[-1]
    tb = float(day_before_row['total_balance'])
    pq = float(day_before_row['portfolio_quantity'])
    pp = float(day_before_row['portfolio_price'])
    dc = float(day_before_row['daily_change'])
    ac = float(day_before_row['acc_change'])
    d = float(day_before_row['deposit'])
    td = float(day_before_row['total_deposits'])
    p = float(day_before_row['profit'])
else:
    tb = 254
    pq = 254/209.2305
    pp = 209.2305
    dc = 0
    ac = 0
    d = 0
    td = 254
    p = 0
if today_day == 25:
    tb = tb + 255
    pq = pq + (255/pp)
    d = 255
    td = td + 255

dc = (portfolio_price - pp) / pp
ac = ac + dc
p = tb - td

new_row = [today_date, tb, pq, pp, dc, ac, d, td, p]

df2 = df.append(pd.DataFrame([new_row], columns=['date','total_balance', 'portfolio_quantity', 'portfolio_price' ,'daily_change','acc_change','deposit','total_deposits','profit']), ignore_index=True)

df2.to_csv("StockIndex.csv")