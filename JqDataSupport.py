# encoding: UTF-8
import jqdatasdk
import time
import talib
import numpy as np

class SupportJqData():

    def __init__(self):
        jqdatasdk.auth(username='13268108673', password='king20110713')

    def getDataFrame(self, security, frequency, count=200, end_date=None):
        try:
            if security is None:
                return None
            if end_date is None:
                end_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            df = jqdatasdk.get_price(
                security=security,
                count=count,
                end_date=end_date,
                frequency=frequency,
                fields=['close', 'open', 'volume', 'high', 'low', 'money']
            )
        except:
            jqdatasdk.auth(username='13824472562', password='472562')
            df = jqdatasdk.get_price(
                security=security,
                count=100,
                end_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                frequency=frequency,
                fields=['close', 'open', 'volume', 'high', 'low', 'money']
            )
        close = [float(x) for x in df['close']]
        df['EMA5']  = talib.EMA(np.array(close), timeperiod=5)
        df['EMA10'] = talib.EMA(np.array(close), timeperiod=10)
        df['EMA20'] = talib.EMA(np.array(close), timeperiod=20)
        df['EMA40'] = talib.EMA(np.array(close), timeperiod=40)
        df['EMA60'] = talib.EMA(np.array(close), timeperiod=60)
        return df

    def getPricePosi(self, df):
        arr = self.getPricePosis(df)
        return arr[-1]

    def getPricePosis(self, df):
        indexList = df[df.EMA60 == df.EMA60].index.tolist()
        pricePositions = []
        for index in indexList:
            ema5 = df.loc[index, 'close']
            emas = sorted(
                [ema5, df.loc[index, 'EMA10'], df.loc[index, 'EMA20'], df.loc[index, 'EMA40'],
                 df.loc[index, 'EMA60']],
                reverse=True)
            pricePosi = 0
            for ema in emas:
                if ema == ema5:
                    break
                pricePosi = pricePosi + 1
            pricePositions.append(pricePosi)
        return pricePositions

    def getRate(self, df):
        indexList = df[df.EMA60 == df.EMA60].index.tolist()
        close = df.loc[indexList[-1], 'close']
        pre_close = df.loc[indexList[-2], 'close']
        return round((close - pre_close)/pre_close, 4) * 100

    def getVolumeArrow(self, df):
        indexList = df[df.EMA60 == df.EMA60].index.tolist()
        volumes = []
        for index in indexList:
            v = df.loc[index, 'volume']
            volumes.append(v)
        count = 0
        max = None
        while count < indexList.__len__() - 1:
            v = volumes[indexList.__len__() - count - 1]
            if max is None:
                max = v
            elif v > max:
                return count - 1
            count = count + 1
        return count - 1