
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: to read and import data                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: CristinaCruzD                                                                     -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import glob
import yfinance as yf
from os import listdir, path
from os.path import isfile, join
import time
import numpy as np
from datetime import timedelta, datetime
from functions import get_data

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

abspath = path.abspath('files/NAFTRAC_holdings')
all_files = [f[:-4] for f in listdir(abspath) if isfile(join(abspath, f))]
all_files = sorted(all_files,key= lambda string: datetime.strptime(string[8:], '%d%m%y') )

data_archivos = get_data(all_files)

i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in all_files])]
i_fechas_com = [pd.to_datetime(i)+timedelta(days=1) for i in i_fechas] # fecha de compra
# Descargar y acomodar datos


tickers = []
for i in all_files:
    l_tickers = list(data_archivos[i]['Ticker'])
    [tickers.append(i + '.MX') for i in l_tickers]
global_tickers = np.unique(tickers).tolist()

global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

[global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX','KOFUBL.MX' ,'BSMXB.MX']]


data = yf.download(global_tickers, start="2017-12-30", end="2020-09-01", actions=False,
                   group_by="close", interval='1d', auto_adj=False, prepost=False, threads=False)

# convertir columna de fechas
data_close = pd.DataFrame({i: data[i]['Close'] for i in global_tickers})
data_open = pd.DataFrame({i: data[i]['Open'] for i in global_tickers})

# tomar solo las fechas de interes (utilizando conjuntos)
ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))

# fechas para inv. activa
daterange = pd.date_range(start=ic_fechas[0],end=ic_fechas[-1]).tolist()

# localizar todos los precios
precios = data_close.iloc[[int(np.where(data_close.index == i)[0]) for i in i_fechas]]
precios_open = data_open.iloc[[int(np.where(data_close.index == i)[0]) for i in i_fechas]]
precios_diarios = data_close.iloc[[int(np.where(data_close.index == i)[0]) for i in daterange]]

