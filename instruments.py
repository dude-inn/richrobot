"""
Модуль для работы с тикерами, figi и свечами.
"""

import json
import datetime
import numpy as np
import vectorbt as vbt
from ta.trend import macd_diff, sma_indicator
from ta.volatility import average_true_range
from datetime import datetime, timedelta
from tinkoff.invest import InstrumentStatus
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest import Client, CandleInterval, HistoricCandle
from pandas import DataFrame
from account_data import TINKOFF_TOKEN
from settings import (STOCK_FEE, MACD_FAST, MACD_SLOW,
                      MACD_INDICATOR, UT_BOT_ATR_PERIOD,
                      UT_BOT_SENSITIVITY, logger)


def cast_money(v) -> float:
    """
    Функция для преобразования Quotation в int
    :param v:
    :return: float
    """
    return v.units + v.nano / 1e9


def getfigi_by_request(ticker):
    """
    Функция возвращает figi акции по ее тикеру.
    :param ticker:
    :return:
    """
    with Client(TINKOFF_TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        r = DataFrame(
            instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE).instruments,
            columns=['name', 'figi', 'ticker', 'class_code']
        )
    r = r[r['ticker'] == ticker]['figi'].iloc[0]
    return r


def get_figi_by_json_file(ticker):
    """
    Функция возвращает figi акции по ее тикеру.
    Запрос идет через файл stocks_data.json
    :param ticker:
    :return:
    """
    with open(file='stocks_data.json', mode='r') as f:
        text = json.load(f)
    for item in text:
        if item['ticker'] == ticker:
            return item['figi']


def get_ticker_by_json_file(figi):
    """
    Функция возвращает ticker акции по ее figi.
    Запрос идет через файл stocks_data.json
    :param figi:
    :return:
    """
    with open(file='stocks_data.json', mode='r') as f:
        text = json.load(f)
    for item in text:
        if item['figi'] == figi:
            return item['ticker']


def get_stocks_from_json_file():
    """
    Функция возвращает список акций из файла stocks_data.json.
    :return:
    """
    logger.info('Работа функции get_stocks_from_json_file')
    with open(file='stocks_data.json', mode='r') as f:
        text = json.load(f)
    return text


def getinstruments_of_TQBR():
    """
    Функция записывающая в файл stocks_data.
    Информацию по акциям (имя, тикер, figi), торгующихся
    на московской бирже
    :return: None
    """
    with Client(TINKOFF_TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        r = DataFrame(
            instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments,
            columns=['ticker', 'name', 'figi', 'class_code', 'api_trade_available_flag', 'buy_available_flag']
        )
    r = r[r['class_code'] == 'TQBR']
    r = r[r['api_trade_available_flag'] == True]
    r = r[r['buy_available_flag'] == True]
    json_file = r.to_json(orient='records')
    with open('stocks_data.json', 'w', encoding='utf8', newline='') as f:
        f.write(json_file)


def create_df(candles: [HistoricCandle]):
    """
    Функция возвращающая DataFrame по свечкам.
    :param candles:
    :return:
    """
    list_df = []
    for candle in candles:
        diff = cast_money(candle.high - candle.low)
        double_fee = cast_money(candle.high) * STOCK_FEE * 2
        how_many_fee_in_diff = round(diff / double_fee, 2)
        list_df.append({'time': candle.time,
                        'volume': candle.volume,
                        'open': cast_money(candle.open),
                        'close': cast_money(candle.close),
                        'high': cast_money(candle.high),
                        'low': cast_money(candle.low),
                        'diff': diff,
                        'double_fee': double_fee,
                        'x_diff_fee': how_many_fee_in_diff
                        })
    return DataFrame(list_df)


def get_5min_candles(figi):
    """
    Функция возвращает DataFrame из 5мин свечей акции.
    :param figi:
    :return:
    """
    with Client(TINKOFF_TOKEN) as client:
        r = client.market_data.get_candles(
            figi=figi,
            from_=datetime.now() - timedelta(days=3),
            to=datetime.now() - timedelta(days=2),
            interval=CandleInterval.CANDLE_INTERVAL_5_MIN
        )
    return create_df(r.candles)


def get_15min_candles(figi):
    """
    Функция возвращает DataFrame из 15мин свечей акции.
    :param figi:
    :return:
    """
    with Client(TINKOFF_TOKEN) as client:
        r = client.market_data.get_candles(
            figi=figi,
            from_=datetime.now() - timedelta(days=4),
            to=datetime.now() - timedelta(days=3),
            interval=CandleInterval.CANDLE_INTERVAL_15_MIN
        )
    return create_df(r.candles)


def xATRTrailingStop_func(close, prev_close, prev_atr, nloss):
    """
    Функция вычисляющая ATRTrailingStop.
    :param close:
    :param prev_close:
    :param prev_atr:
    :param nloss:
    :return:
    """
    if close > prev_atr and prev_close > prev_atr:
        return max(prev_atr, close - nloss)
    elif close < prev_atr and prev_close < prev_atr:
        return min(prev_atr, close + nloss)
    elif close > prev_atr:
        return close - nloss
    else:
        return close + nloss


def add_indicators_in_df(pd_data):
    """
    Функция добалвяет индикаторы в Dataframe.
    Реализовано добавление macd_diff, xATR,
    сигналов Buy и Sell UT BOT
    :param pd_data:
    :return:
    """
    pd_data['macd_diff'] = macd_diff(
        close=pd_data['close'],
        window_slow=MACD_SLOW,
        window_sign=MACD_INDICATOR,
        window_fast=MACD_FAST
    )
    pd_data['xATR'] = average_true_range(
        high=pd_data['high'],
        low=pd_data['low'],
        close=pd_data['close'],
        window=UT_BOT_ATR_PERIOD
    )
    pd_data['nLoss'] = UT_BOT_SENSITIVITY * pd_data['xATR']
    pd_data['ATRTrailingStop'] = [0.0] + [np.nan for i in range(len(pd_data) - 1)]
    for i in range(1, len(pd_data)):
        pd_data.loc[i, 'ATRTrailingStop'] = xATRTrailingStop_func(
            pd_data.loc[i, 'close'],
            pd_data.loc[i - 1, 'close'],
            pd_data.loc[i - 1, 'ATRTrailingStop'],
            pd_data.loc[i, 'nLoss'],
        )

    ema = vbt.MA.run(pd_data['close'], 1, short_name='EMA', ewm=True)
    pd_data['Above'] = ema.ma_crossed_above(pd_data['ATRTrailingStop'])
    pd_data['Below'] = ema.ma_crossed_below(pd_data['ATRTrailingStop'])
    pd_data['Buy'] = (pd_data['close'] > pd_data['ATRTrailingStop']) & (pd_data['Above'] == True)
    pd_data['Sell'] = (pd_data['close'] < pd_data['ATRTrailingStop']) & (pd_data['Below'] == True)

getinstruments_of_TQBR()
