import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time 

from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from tqdm.notebook import trange
from TaPR_pkg import etapr
from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping

# 데이터 불러오는 코드 
# sorted = 정렬
TRAIN_DATASET = sorted([x for x in Path("D:\\AI\\data\\dataset\\HAI 2.0\\training").glob("*.csv")])
TEST_DATASET = sorted([x for x in Path("D:\\AI\\data\\dataset\\HAI 2.0\\testing").glob("*.csv")])
VALIDATION_DATASET = sorted([x for x in Path("D:\\AI\\data\\dataset\\HAI 2.0\\validation").glob("*.csv")])
# engine ='python' = 사용할 언어 설정 
def dataframe_from_csv(target):
    return pd.read_csv(target,engine='python').rename(columns=lambda x: x.strip())

def dataframe_from_csvs(targets):
    return pd.concat([dataframe_from_csv(x) for x in targets])

TRAIN_DF_RAW = dataframe_from_csvs(TRAIN_DATASET)

TIMESTAMP_FIELD = 'time'
IDSTAMP_FIELD ='id'
ATTACK_FIELD = 'attack'
VALID_COLUMNS_IN_TRAIN_DATASET = TRAIN_DF_RAW.columns.drop([TIMESTAMP_FIELD])
# print(VALID_COLUMNS_IN_TRAIN_DATASET)

# 데이터 정규화
TAG_MIN = TRAIN_DF_RAW[VALID_COLUMNS_IN_TRAIN_DATASET].min()
TAG_MAX = TRAIN_DF_RAW[VALID_COLUMNS_IN_TRAIN_DATASET].max()

def normalize(df):
    ndf = df.copy()
    for c in df.columns:
        if TAG_MIN[c] == TAG_MAX[c]:
            ndf[c] = df[c] - TAG_MIN[c]
        else:
            ndf[c] = (df[c]- TAG_MIN[c]) / (TAG_MAX[c] - TAG_MIN[c])
    return ndf

TRAIN_DF = normalize(TRAIN_DF_RAW[VALID_COLUMNS_IN_TRAIN_DATASET])

def boundary_check(df):
    x = np.array(df, dtype= np.float32)
    print(x)
    return np.any(x >1.0),np.any(x <0), np.any(np.isnan(x))

boundary_check(TRAIN_DF)

def temporalize(X, y, timesteps):
    output_X = []
    output_y = []
    for i in range(len(X) - timesteps -1):
        t= []
        for j in range(1, timesteps +1):
            t.append(X[[i + j + 1], :])
        output_X.append(t)
        output_y.append(y[i + timesteps + 1])
    return np.squeeze(np.array(output_X)), np.array(output_y)

train = np.array(TRAIN_DF)
x_train = train.reshape(train.shape[0], 1, train.shape[1])
# print(x_train.shape)        

                    