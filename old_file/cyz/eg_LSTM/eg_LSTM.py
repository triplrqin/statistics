'''
Example of LSTM using Keras : https://medium.com/@daniel820710/%E5%88%A9%E7%94%A8keras%E5%BB%BA%E6%A7%8Blstm%E6%A8%A1%E5%9E%8B-%E4%BB%A5stock-prediction-%E7%82%BA%E4%BE%8B-1-67456e0a0b
'''
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM, TimeDistributed, RepeatVector
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

# 读取csv文件的资料
def readTrain():
    train = pd.read_csv("SPY.csv")
    return train

# 除了基本資料提供的Features(Open, High, Low, Close, Adj Close, Volume)以外，還可自己增加Features，例如星期幾、幾月、幾號等等
def augFeatures(train):
    train["Date"] = pd.to_datetime(train["Date"])
    train["year"] = train["Date"].dt.year
    train["month"] = train["Date"].dt.month
    train["date"] = train["Date"].dt.day
    train["day"] = train["Date"].dt.dayofweek
    return train

# Nomralization 將所有資料做正規化，而由於Date 是字串非數字，因此先將它drop掉
def normalize(train):
    train = train.drop(["Date"], axis=1)
    # axis=0 表示针对每一列
    train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)), axis=0)
    return train_norm

# 輸入X_train: 利用前30天的Open, High, Low, Close, Adj Close, Volume, month, year, date, day作為Features，shape為(30, 10)
# 輸出Y_train: 利用未來5天的Adj Close作為Features，shape為(5,1)

def buildTrain(train, pastDay=30, futureDay=5):
    X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
        X_train.append(np.array(train.iloc[i:i+pastDay]))
        Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Adj Close"]))
    return np.array(X_train), np.array(Y_train)

# 將資料打散，而非照日期排序
def shuffle(X,Y):
    np.random.seed(10)
    randomList = np.arange(X.shape[0])
    np.random.shuffle(randomList)
    return X[randomList], Y[randomList]

# 將Training Data取一部份當作Validation Data

def splitData(X,Y,rate):
    X_train = X[int(X.shape[0]*rate):]
    Y_train = Y[int(Y.shape[0]*rate):]
    X_val = X[:int(X.shape[0]*rate)]
    Y_val = Y[:int(Y.shape[0]*rate)]
    return X_train, Y_train, X_val, Y_val

'''
# 准备训练数据和验证数据
# read SPY.csv
train = readTrain()

# Augment the features (year, month, date, day)
train_Aug = augFeatures(train)

# Normalization
train_norm = normalize(train_Aug)

# build Data, use last 30 days to predict next 5 days
X_train, Y_train = buildTrain(train_norm, 30, 5)

# shuffle the data, and random seed is 10
X_train, Y_train = shuffle(X_train, Y_train)

# split training data and validation data
X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)
# X_train: (5710, 30, 10)
# Y_train: (5710, 5, 1)
# X_val: (634, 30, 10)
# Y_val: (634, 5, 1)
'''


# 建立one-to-one模型
def buildOneToOneModel(shape):
    model = Sequential()
    model.add(LSTM(10, input_length=shape[1], input_dim=shape[2],return_sequences=True))
    # output shape: (1, 1)
    model.add(TimeDistributed(Dense(1)))    # or use model.add(Dense(1))
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    return model


# train = readTrain()
# train_Aug = augFeatures(train)
# train_norm = normalize(train_Aug)
# # change the last day and next day 
# X_train, Y_train = buildTrain(train_norm, 1, 1)
# X_train, Y_train = shuffle(X_train, Y_train)
# X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

# # from 2 dimmension to 3 dimension
# Y_train = Y_train[:,np.newaxis]
# Y_val = Y_val[:,np.newaxis]
# model = buildOneToOneModel(X_train.shape)
# callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")
# model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])


# 建立many-to-one模型
def buildManyToOneModel(shape):
    model = Sequential()
    # 第一个参数代表LSTM的dimension,即输出类似于对feature_dimesion的变换 eg. 10 -> 100 -> 10 -> 1
    model.add(LSTM(100, input_length=shape[1], input_dim=shape[2], return_sequences=True))
    model.add(LSTM(10))
    # output shape: (1, 1)
    model.add(Dense(1))
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    return model


train = readTrain()
train_Aug = augFeatures(train)
train_norm = normalize(train_Aug)
# change the last day and next day 
X_train, Y_train = buildTrain(train_norm, 30, 1)
X_train, Y_train = shuffle(X_train, Y_train)
# because no return sequence, Y_train and Y_val shape must be 2 dimension
X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

model = buildManyToOneModel(X_train.shape)
callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")
model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])


# one-to-many 模型

def buildOneToManyModel(shape):
    model = Sequential()
    model.add(LSTM(10, input_length=shape[1], input_dim=shape[2]))
    # output shape: (5, 1)
    model.add(Dense(1))
    model.add(RepeatVector(5))
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    return model

# many-to-many 模型
# 比如以过去30天预测未来5天
def buildManyToManyModel(shape):
    model = Sequential()
    model.add(LSTM(10, input_shape=(shape[1],shape[2]), return_sequences=True))
    # output shape: (5, 1)
    model.add(TimeDistributed(Dense(1)))
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    return model


# train = readTrain()
# train_Aug = augFeatures(train)
# train_norm = normalize(train_Aug)
# # change the last day and next day 
# X_train, Y_train = buildTrain(train_norm, 5, 5)
# X_train, Y_train = shuffle(X_train, Y_train)
# X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

# # from 2 dimmension to 3 dimension
# Y_train = Y_train[:,:,np.newaxis]
# Y_val = Y_val[:,:,np.newaxis]

# model = buildManyToManyModel(X_train.shape)
# callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")
# model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])