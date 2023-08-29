# Importando las bibliotecas necesarias
import requests
import pandas as pd
from datetime import date
from time import sleep

# Verificando si el archivo CSV "StockIndex.csv" existe
fileExist = True
try:
    df = pd.read_csv("StockIndex.csv")
except:
    fileExist = False
    print('Warning!: CSV File does not exists')

# Si el archivo no existe, se crea un DataFrame vacío con las columnas especificadas
if fileExist is False:
    df = pd.DataFrame(columns=['date', 'total_balance', 'portfolio_quantity', 'portfolio_price',
                      'daily_change', 'acc_change', 'deposit', 'total_deposits', 'profit'])

# Obteniendo la fecha actual
today_date = date.today()
today_day = today_date.day

# Definiendo variables constantes
monthly_deposit = 255
apiKey = 'TYN58ZBCTHT1ZLK3'
tickers = ["VOO", "VTI", "VTIP", "VGSH", "BRK.B", "ICLN"]

# Diccionario para almacenar los precios actuales de las acciones
portfolio = {}

# Diccionario de precios dummy para pruebas
dummyDict = {'VOO': 412.6400, 'VTI': 223.1900, 'VTIP': 47.3400,
             'VGSH': 57.7500, 'BRK.B': 358.2900, 'ICLN': 16.5400}

# Si dummy es False, se obtienen los precios actuales de las acciones desde la API de AlphaVantage
if dummy == False:
    for ticker in tickers:
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + \
            ticker + '&apikey=' + apiKey
        r = requests.get(url)
        sleep(13)  # Espera 13 segundos para evitar limitaciones de la API
        data = r.json()
        portfolio[ticker] = float(data['Global Quote']['05. price'])
else:
    portfolio = dummyDict

print(portfolio)

# Proporciones de cada acción en el portafolio
proportions = {"VOO": 0.3, "VTI": 0.2, "VTIP": 0.1,
               "VGSH": 0.3, "BRK.B": 0.05, "ICLN": 0.05}

# Calculando el precio del portafolio basado en las proporciones y precios actuales
portfolio_price = 0
for ticker in tickers:
    print(proportions[ticker])
    p = portfolio[ticker]
    portfolio_price = portfolio_price + p * proportions[ticker]

# Si el archivo CSV existía, se obtienen los valores del día anterior
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
else:  # Si no, se establecen valores predeterminados
    tb = 254
    pq = 254/209.2305
    pp = 209.2305
    dc = 0
    ac = 0
    d = 0
    td = 254
    p = 0

# Si es el día 25 del mes, se añade el depósito mensual
if today_day == 25:
    tb = tb + 255
    pq = pq + (255/pp)
    d = 255
    td = td + 255

# Calculando el cambio diario y acumulado
dc = (portfolio_price - pp) / pp
ac = ac + dc
p = tb - td

# Creando una nueva fila con los datos del día
new_row = [today_date, tb, pq, pp, dc, ac, d, td, p]

# Añadiendo la nueva fila al DataFrame y guardando en el archivo CSV
df2 = df.append(pd.DataFrame([new_row], columns=['date', 'total_balance', 'portfolio_quantity',
                'portfolio_price', 'daily_change', 'acc_change', 'deposit', 'total_deposits', 'profit']), ignore_index=True)
df2.to_csv("StockIndex.csv")
