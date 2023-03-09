"""
main.py
利用日线指数与情感指数进行股票预测
"""
import tushare as ts
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM
from keras import regularizers
import keras
import os
# from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras.layers import Dense, Dropout, Activation
# from tensorflow.keras.layers import LSTM
# from tensorflow.keras import regularizers
# import tensorflow.keras

import time
import matplotlib.pyplot as pyplot
import xlrd
import xlwt


def dataget(start_date, end_date, code):
    """
    数据获取
    :param start_date: string
    :param end_date: string
    :param code: string
    :return: ndarray
    """
    # ts.set_token("64acacc4d6dc7fa5cf368ac432f069ba3d041ed0aff877733443585f")
    ts.set_token("65e348fe68950a0138871639589e8646fe387486e6105e195da9c7bb")
    pro = ts.pro_api()
    # df = pro.index_daily(ts_code=code, start_date=start_date, end_date=end_date,
    #                      fields='trade_date,close,open,high,low,vol,amount,pct_chg')
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date,
                         fields='trade_date,close,open,high,low,vol,amount,pct_chg')
    length = df.shape[0]

    print('length:'+str(length))
    data = []
    if not length:
        return data
    for i in range(length):
        each_data = [df.loc[length - 1 - i]['trade_date'], df.loc[length - 1 - i]['open'],
                     df.loc[length - 1 - i]['close'], df.loc[length - 1 - i]['low'],
                     df.loc[length - 1 - i]['high'], df.loc[length - 1 - i]['vol'],
                     df.loc[length - 1 - i]['amount'], df.loc[length - 1 - i]['pct_chg']]
        each_data = np.array(each_data, dtype='float64')
        data.append(each_data)
    data = np.array(data, dtype='float64')
    print('数据类型：', type(data))
    print('数据个数：', data.shape[0])
    print('数据形状：', data.shape)
    print('数据第一行：', data[0])
    return data


def mooddataget():
    """
    情感数据获取
    :return: ndarray
    """
    # 从excel中获取已经得到的情感数据
    read = xlrd.open_workbook("mood.xls")
    sheet = read.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    print(rows)
    print(cols)
    mood_data = []
    for i in range(rows):
        each_data1 = sheet.row_values(i)
        each_data1 = np.array(each_data1, dtype="float64")
        mood_data.append(each_data1)
    mood_data = np.array(mood_data, dtype="float64")
    print('数据类型：', type(mood_data))
    print('数据个数：', mood_data.shape[0])
    print('数据形状：', mood_data.shape)
    print('数据第一行：', mood_data[0])
    return mood_data, rows


def datacombine(data1, data2, len1, len2):
    """
    数据合并
    利用两个矩阵中的日期label进行数据合并，避开节假日
    :param data1: ndarray 情感数据
    :param data2: ndarray 日线数据
    :param len1: int 情感数
    :param len2: int 日线数
    :return: ndarray
    """
    i, j = 0, 0
    data = []
    while i < len1 and j < len2:
        if data1[i][0] == data2[j][0]:
            data3 = np.hstack((data2[j][1:8], data1[i][1:3]))
            data.append(data3)
            i += 1
            j += 1
        else:
            i += 1
    data = np.array(data, dtype="float64")
    print(i, j)
    print('数据类型：', type(data))
    print('数据个数：', data.shape[0])
    print('数据形状：', data.shape)
    print('数据第一行：', data[0])
    return data


def valuestore(data):
    """
    数据集参数存储
    :param data: ndarray
    :return: list
    """
    value = []
    value.append(np.max(data[:, 2]))
    value.append(np.mean(data[:, 2]))
    value.append(np.min(data[:, 2]))
    return value