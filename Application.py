# encoding: UTF-8

from flask import Flask, render_template, request
import json
import Util as util
import ProgramAndMe_ConnectionUnit as pamConn
from JqDataSupport import SupportJqData as sjd
app = Flask(__name__)

supportJqData = sjd()

# 页面----------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    fs = ['CF9999.XZCE', 'MA9999.XZCE', 'RM9999.XZCE', 'SF9999.XZCE', 'SM9999.XZCE',
          'TA9999.XZCE', 'ZC9999.XZCE', 'AP9999.XZCE', 'JM9999.XDCE', 'L9999.XDCE',
          'M9999.XDCE', 'PP9999.XDCE', 'V9999.XDCE', 'HC9999.XSGE', 'RB9999.XSGE', 'FU9999.XSGE', 'BU9999.XSGE']
    retArr = []
    for fu in fs:
        df = supportJqData.getDataFrame(security=fu, frequency='15m')
        priceposi = supportJqData.getPricePosi(df)
        volumearrow = supportJqData.getVolumeArrow(df)
        rate = supportJqData.getRate(df)
        value = 1
        if priceposi == 0 or priceposi == 4:
            value = value * 4
        else:
            value = value * 2
        value = value * volumearrow + 1
        retArr.append({'security': fu, 'rate': rate, 'priceposi': priceposi, 'volumearrow': volumearrow, 'value': value})

    return render_template('index.html', title='listener', data=json.dumps(retArr))

#上期所
#
# 代码	名称	代码	名称
# AG9999.XSGE	白银主力合约	PB9999.XSGE	铅主力合约
# AU9999.XSGE	黄金主力合约	RB9999.XSGE	螺纹钢主力合约
# AL9999.XSGE	铝主力合约	RU9999.XSGE	天然橡胶主力合约
# BU9999.XSGE	沥青主力合约	SN9999.XSGE	锡主力合约
# CU9999.XSGE	铜主力合约	WR9999.XSGE	线材主力合约
# FU9999.XSGE	燃油主力合约	ZN9999.XSGE	锌主力合约
# HC9999.XSGE	热卷主力合约	NI9999.XSGE	镍主力合约
# 郑商所
#
# 代码	名称	代码	名称
# CY9999.XZCE	棉纱主力合约	RM9999.XZCE	菜籽粕主力合约
# CF9999.XZCE	棉花主力合约	RM9999.XZCE	菜籽粕主力合约
# FG9999.XZCE	玻璃主力合约	RS9999.XZCE	油菜籽主力合约
# JR9999.XZCE	粳谷主力合约	SF9999.XZCE	硅铁主力合约
# LR9999.XZCE	晚稻主力合约	SM9999.XZCE	锰硅主力合约
# MA9999.XZCE	甲醇主力合约	SR9999.XZCE	白糖主力合约
# TA9999.XZCE	PTA主力合约
# OI9999.XZCE	菜油主力合约
# PM9999.XZCE	普麦主力合约	ZC9999.XZCE	动力煤主力合约
# AP9999.XZCE	苹果主力合约
# 大商所
#
# 代码	名称	代码	名称
# A9999.XDCE	豆一主力合约	JD9999.XDCE	鸡蛋主力合约
# B9999.XDCE	豆二主力合约	JM9999.XDCE	焦煤主力合约
# BB9999.XDCE	胶板主力合约	L9999.XDCE	聚乙烯主力合约
# C9999.XDCE	玉米主力合约	M9999.XDCE	豆粕主力合约
# CS9999.XDCE	淀粉主力合约	P9999.XDCE	棕榈油主力合约
# FB9999.XDCE	纤板主力合约	PP9999.XDCE	聚丙烯主力合约
# I9999.XDCE	铁矿主力合约	V9999.XDCE	聚氯乙烯主力合约
# J9999.XDCE	焦炭主力合约	Y9999.XDCE	豆油主力合约
@app.route('/candle_sticks')
def candle_sticks():
    args = request.args
    security = str(args.get('security'))
    frequency = str(args.get('frequency'))
    endtime = str(args.get('endtime'))
    nowTimeString = util.getYMDHMS()
    if frequency is None or frequency == 'None':
        frequency = '15m'
    if endtime is not None and endtime != '':
        df = supportJqData.getDataFrame(security=security, frequency=frequency, count=130, end_date=endtime)
    else:
        df = supportJqData.getDataFrame(security=security, frequency=frequency, count=130)
    indexList = df.index.tolist()
    retArr = []
    for index in indexList:
        time = str(index)
        volume = df.loc[index, 'volume']
        max = df.loc[index, 'high']
        min = df.loc[index, 'low']
        start = df.loc[index, 'open']
        end = df.loc[index, 'close']
        money = df.loc[index, 'money']
        retArr.append({'time': time, 'start': start, 'end': end, 'max': max, 'min': min, 'volume': volume, 'money': money})
    return render_template('candle-sticks.html', data=json.dumps(retArr), security=security, nowTimeString=nowTimeString, pageActionName0='candle_sticks')

@app.route('/waiting_judge_items')
def waiting_judge_items():
    asking_data = pamConn.getAskingData()
    return render_template('waiting-judge-items.html', asking_data=json.dumps(asking_data))

# 动作-------------------------------------------------------------------------------------------------
@app.route('/action_permit_trade')
def action_permit_trade():
    args = request.args
    security = str(args.get('security'))
    pamConn.permit(security)
    return 'OK'

@app.route('/action_deny_trade')
def action_deny_trade():
    args = request.args
    security = str(args.get('security'))
    pamConn.deny(security)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5288)
    #security = "HC9999.XSGE"
    #df = getDataFrame(security=security, frequency='5m')
    # print getPricePosi(df)
    #print security + ": va->" + str(getVolumeArrow(df)) + " pp->" + str(getPricePosi(df))