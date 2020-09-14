
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab1 Passive and Active Investing                                                       -- #
# -- script: main.py : Development of investing strategies                                        -- #
# -- author: CristinaCruzD                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
from data import all_files, data_archivos,precios, i_fechas, data_close, data_open, precios_open, precios_diarios, daterange,data


######## df pasiva
df_pasiva = pd.DataFrame(index= np.arange(0,len(all_files)+1),columns=['timestamp','capital', 'rend', 'rend_acum'])
k = 1000000
# comisiones
c = 0.00125
df_pasiva.capital[0]=k
df_pasiva.timestamp[0] = '2018-01-30'
df_pasiva.timestamp[1:] = i_fechas

pos_datos = data_archivos[all_files[0]][['Ticker', 'Nombre', 'Peso (%)']]
pos_datos=pd.DataFrame(pos_datos)
c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']            #tickers a eliminar
pos_datos.drop(list(pos_datos[list(pos_datos['Ticker'].isin(c_activos))].index), inplace=True)  # eliminar tickers
pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'
pos_datos['Ticker'] = pos_datos['Ticker'].replace(['LIVEPOLC.1.MX','MEXCHEM.MX','GFREGIOO.MX'],
                                                      ['LIVEPOLC-1.MX','ORBIA.MX','RA.MX'])
pos_datos['Precio'] = [precios.iloc[0, precios.columns.to_list().index(j)] for j in pos_datos['Ticker']]
pos_datos['Capital'] = pos_datos['Peso (%)'] * k - pos_datos['Peso (%)'] * k * c
pos_datos['Titulos'] = np.round(pos_datos['Capital'] / pos_datos['Precio'])
pos_datos['Postura'] = pos_datos['Titulos']*pos_datos['Precio']
pos_datos['Comision'] = pos_datos['Postura'] * c
pos_cash = k - pos_datos['Postura'].sum() - pos_datos['Comision'].sum()
df_pasiva.capital[1] = pos_datos['Postura'].sum() + pos_cash
for i in range(1,len(all_files)):
    precio= [precios.iloc[i, precios.columns.to_list().index(j)] for j in pos_datos['Ticker']]
    postura = pos_datos['Titulos']*precio
    df_pasiva.capital[i+1] = postura.sum()+pos_cash

df_pasiva.rend = df_pasiva.capital/df_pasiva.capital.shift(1)-1
df_pasiva.rend_acum = np.cumsum(df_pasiva.rend)

######## df activa

df_activa = pd.DataFrame(index= np.arange(0,len(all_files)+1),columns=['timestamp','capital', 'rend', 'rend_acum'])
k = 1000000
c = 0.00125
df_activa.capital[0]=k
df_activa.timestamp[0] = '2018-01-30'
df_activa.timestamp[1:] = i_fechas
df_operaciones = pd.DataFrame(columns=['timestamp', 'titulos_totales', 'titulos_compra',
                              'precio', 'comision','comision_acum'])
#identificar el activo con mayor participación:

mayor = pos_datos[pos_datos['Peso (%)'] == max(pos_datos['Peso (%)'])]['Ticker'][0] # devuelve el ticker
act_datos = data_archivos[all_files[0]][['Ticker', 'Nombre', 'Peso (%)']]
act_datos=pd.DataFrame(act_datos)
c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']            #tickers a eliminar
act_datos.drop(list(act_datos[list(act_datos['Ticker'].isin(c_activos))].index), inplace=True)  # eliminar tickers
act_datos['Ticker'] = act_datos['Ticker'] + '.MX'
act_datos['Ticker'] = act_datos['Ticker'].replace(['LIVEPOLC.1.MX','MEXCHEM.MX','GFREGIOO.MX'],
                                                      ['LIVEPOLC-1.MX','ORBIA.MX','RA.MX'])
act_datos['Peso (%)'] = act_datos['Peso (%)'].replace(act_datos['Peso (%)'][act_datos.Ticker==mayor][0],
                                                          act_datos['Peso (%)'][act_datos.Ticker==mayor][0]/2)

act_datos['Precio'] = [precios.iloc[0, precios.columns.to_list().index(j)] for j in act_datos['Ticker']]
act_datos['Capital'] = act_datos['Peso (%)'] * k - act_datos['Peso (%)'] * k * c
act_datos['Titulos'] = np.round(act_datos['Capital'] / act_datos['Precio'])
act_datos['Postura'] = act_datos['Titulos']*act_datos['Precio']
act_datos['Comision'] = act_datos['Postura'] * c

act_cash = k - act_datos['Postura'].sum() - act_datos['Comision'].sum()
df_activa.capital[1] = act_datos['Postura'].sum() + act_cash

for i in range(len(daterange)):
    if precios_open[mayor][i]>precios[mayor][i]:
        df_operaciones.timestam[i] = daterange[i+1]
        df_operaciones.titulos_compra[i] = act_cash/precios_diarios[i+1]
        df_operaciones.precio[i]=precios_diarios[i+1]
        df_operaciones.comisiones[i] = precios_diarios[i+1] + df_operaciones.titulos_compra[i]*c


