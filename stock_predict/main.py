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


def slicewindow(data):
    """
    滑窗读取数据，得到形状为（n，30，7）的数组
    :param data: ndarray
    :return: ndarray
    """
    step = 30  # 改变预测输入时间序列的长度
    x, y = [], []
    length = data.shape[0]
    for i in range(length - 30):
        end = i + step
        one_x = data[i:end, :]
        one_y = data[end, 1]
        x.append(one_x)
        y.append(one_y)
    return np.array(x, dtype='float64'), np.array(y, dtype='float64')


def datasplit(data):
    """
    数据分割
    :param data: ndarry
    :return: ndarray
    """
    radio = 0.8     # 分割比
    data, label = slicewindow(data)
    train_size = int(data.shape[0] * radio)
    train_data = data[0:train_size, :]
    train_label = label[0:train_size]
    test_data = data[train_size:, :]
    test_label = label[train_size:]
    print("train_data:", train_data.shape)
    print("train_label:", train_label.shape)
    print("test_data:", test_data.shape)
    print("test_label:", test_label.shape)
    return train_data, train_label, test_data, test_label


def normalization(data):
    """
    归一化
    归一化与只用日线数据略有改变，因矩阵中增加了日期标签，在归一化时应避开日期
    :param data: ndarray
    :return: ndarray
    """
    avg = np.mean(data[:, 1:], axis=0)  # axis=0表示按数组元素的列对numpy取相关操作值
    max_ = np.max(data[:, 1:], axis=0)
    min_ = np.min(data[:, 1:], axis=0)
    print("max", type(max_))
    print(max_.shape)
    data[:, 1:] = (data[:, 1:] - avg) / (max_ - min_)
    return data


def datanormalization(train_data, train_label, test_data, test_label):
    """
    归一化
    归一化与只用日线数据略有改变，因矩阵中增加了日期标签，在归一化时应避开日期
    :param train_data: ndarray
    :param train_label: ndarray
    :param test_data: ndarray
    :param test_label: ndarray
    :return: ndarray
    """
    train_data = normalization(train_data)
    train_label = normalization(train_label)
    test_data = normalization(test_data)
    test_label = normalization(test_label)
    return train_data, train_label, test_data, test_label


def inputnormalization(data, _max, _min, avg):
    """
    输入归一化，如果输入不是原数据集中的数据，须进行相同归一化
    :param data: ndarrar
    :param _max: ndarray
    :param _min: ndarray
    :param avg: ndarray
    :return: ndarray
    """
    return (data - avg) / (_max - _min)


def renormalization(data, _max, _min, avg):
    """
    反归一化，只需对label进行反归一化
    :param data: ndarray
    :param _max: float32
    :param _min: float32
    :param avg: float32
    :return: ndarray
    """
    return data * (_max - _min) + avg


def lstm_model(layers):
    """
    lstm模型建模
    输入参数layers为层数，(layers[0], layers[1])为输入形状，layers[2]为输出形状
    :param layers: list
    :return:
    """
    model = Sequential()
    # LSTM层
    '''
    256个单元 rule激活函数
    return_sequences=True返回整个序列，否则返回输出序列的最后一个输出
    kernel_regularizer正则项/Dropout层--减少过拟合现象
    直接在每层神经元后面添加，0.4这个为Dropout率，可以理解为每个神经元被处理的概率。
    过拟合是指学习时选择的模型所包含的参数过多，以致于出现这一模型对已知数据预测得很好，但对未知数据预测得很差的现象1。
    简单来说，就是模型在训练数据上表现得太好了，以至于无法很好地泛化到新的数据上。
    '''
    #model.add(LSTM(256, activation='relu', return_sequences=False, input_shape=(layers[0], layers[1]),
    #              kernel_regularizer=regularizers.l2(0.000001)))
    model.add(LSTM(256, activation='relu', return_sequences=False, input_shape=(layers[0], layers[1]),
                   kernel_regularizer = regularizers.l2(0.001)))
    model.add(Dropout(0.4))
    # BP层
    model.add(Dense(256))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    # 输出层
    '''
     线性激活函数的输出与输入相同，即 f(x) = x
     '''
    model.add(Dense(layers[2]))
    model.add(Activation("linear"))
    # 优化器
    op = keras.optimizers.Adam()
    # 损失函数
    lo = keras.losses.MeanSquaredLogarithmicError()
    model.compile(optimizer=op, loss=lo)
    return model


if __name__ == '__main__':
    for i in range(1):
        # 获取数据，分别输入开始，结束日期与股票代码
        Code=str(i+1).zfill(6)+'.SZ'
        print('Code:'+Code)
        fileName_1=Code+'_daily_data'+'.txt'
        daily_data = dataget("20190309", "20210308", Code)
        np.savetxt(fileName_1, daily_data)

        filePath = fileName_1
        print('文本字节数'+str(os.path.getsize(filePath)))
        #判断文本文件是否为空。若为空，则删除该文件并跳转到下一次循环；若不为空，则继续执行操作。
        if not os.path.getsize(filePath):
            os.remove(filePath)
            print('股票：'+Code+'已退市！')
            continue

        # 从文本文件中读取数据
        daily_data = np.loadtxt(fileName_1)
        # 存储数据集参数，最大值，平均值与最小值，用于归一化
        data_value = valuestore(daily_data)
        # 先对数据归一化
        daily_data = normalization(daily_data)
        mood_data, mood_len = mooddataget()
        data = datacombine(mood_data, daily_data, mood_len, daily_data.shape[0])
        # 数据分割
        train_data, train_label, test_data, test_label = datasplit(data)
        # 构建模型
        model = lstm_model([30, train_data.shape[2], 1])
        # 模型显示
        model.summary()
        start = time.time()
        # h = model.fit(train_data, train_label, epochs=100, batch_size=71,
        #               validation_data=(test_data, test_label), verbose=1, shuffle=True)
        h = model.fit(train_data, train_label, epochs=100, batch_size=71,
                      validation_data=(test_data, test_label), verbose=1, shuffle=True)
        # 画出损失函数
        print("> Compilation Time : ", time.time() - start)
        pyplot.plot(h.history['loss'], label='train')
        pyplot.plot(h.history['val_loss'], label='test')
        pyplot.legend()
        fileName_2 = Code + '_lossFunction' + '.jpg'
        pyplot.savefig(fileName_2)
        pyplot.show()

        # 保存读取模型
        fileName_3=Code+'_mood_model'+'.h5'
        # model.save('mood_model.h5')
        model.save(fileName_3)
        # model = load_model('mood_model.h5')
        # 输入归一化（如果需要
        # input = inputnormalization(input, data_value[0], data_value[2], data_value[1])
        # 画出预测结果
        # 需要对预测结果进行格式转换（矩阵转置）
        predict = model.predict(test_data)
        predict = predict.transpose()[0]
        # 反归一化
        predict = renormalization(predict, data_value[0], data_value[2], data_value[1])
        test_label = renormalization(test_label, data_value[0], data_value[2], data_value[1])
        pyplot.plot(predict, label='predict')
        pyplot.plot(test_label, label='real')
        pyplot.legend()
        fileName_4 = Code + '_predictFunction' + '.jpg'
        pyplot.savefig(fileName_4)
        pyplot.show()

        fileName_5=Code+'_predict'+'.txt'
        np.savetxt(fileName_5, predict)
        fileName_6 = Code + '_real' + '.txt'
        np.savetxt(fileName_6, test_label)
        err = predict - test_label

        for j in range(err.shape[0]):
            err[j] = err[j] ** 2
        cost = np.mean(err)
        print("均方误差为：", np.sqrt(cost))
