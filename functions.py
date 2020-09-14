"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab1: Passive and Active Investing                                                          -- #
# -- script: functions.py : functions to help the investing process                                         -- #
# -- author: CristinaCruzD                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np


def get_data(all_files):
    data_archivos = {}
    for i in all_files:
        data = pd.read_csv('files/NAFTRAC_holdings/' + i + '.csv', skiprows=2, header=None)
        data.columns = list(data.iloc[0, :])
        data = data.iloc[:, pd.notnull(data.columns)]
        data = data.iloc[1:-1].reset_index(inplace=False, drop=True)
        data['Precio'] = [i.replace(',', '') for i in data['Precio']]
        data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
        convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
        data = data.astype(convert_dict)
        data['Peso (%)'] = data['Peso (%)'] / 100
        data_archivos[i] = data
    return data_archivos


