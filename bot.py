"""
Модуль для работы с торговыми стратегиями.
"""

import time
import threading

from instruments import (get_stocks_from_json_file,
                         get_5min_candles,
                         add_indicators_in_df, get_ticker_by_json_file)
from orders import make_market_order_buy, get_order_state
from telegram_messages import send_telegram_message
from settings import logger, COUNT_OF_OPEN_POSITION, SLEEP_TIME_IF_BUY_LIST_IS_EMPTY


mutex = threading.Lock()
buy_list = []
sell_list = []


def searching_stocks():
    while True:
        for item in get_stocks_from_json_file():
            logger.info(f'Перебор акций: {item["ticker"]}')
            df = get_5min_candles(item['figi'])
            add_indicators_in_df(pd_data=df)
            bool_var_macd_buy = df['macd_diff'].iloc[-2] < 0 and df['macd_diff'].iloc[-1] > 0
            bool_var_macd_buy_filter = (df['macd_diff'].iloc[-3] < 0 and
                                        df['macd_diff'].iloc[-4] < 0 and
                                        df['macd_diff'].iloc[-5] < 0)

            bool_var_UTBOT_buy = df['Buy'].iloc[-1] == True or df['Buy'].iloc[-2] == True
            if bool_var_macd_buy and bool_var_macd_buy_filter and bool_var_UTBOT_buy:
                send_telegram_message(f'К покупке {item["ticker"]}')
                buy_list.append(item['figi'])
                print(df)
            time.sleep(0.5)


def making_orders_to_buy():
    while True:
        if not buy_list:
            time.sleep(SLEEP_TIME_IF_BUY_LIST_IS_EMPTY)
        figi_to_buy = buy_list.pop()
        response_buy = make_market_order_buy(figi=figi_to_buy, quantity=1)
        time.sleep(0.2)


        if response.lots_requested == response.lots_executed:
            message = f"Куплено: {get_ticker_by_json_file(figi_to_buy)}, {1} лотов"
            logger.info(message)
            send_telegram_message(message)
            sell_list.append(figi_to_buy)


def making_orders_to_sell():
    while True:
        if not sell_list:
            time.sleep(SLEEP_TIME_IF_BUY_LIST_IS_EMPTY)
        figi_to_buy = buy_list.pop()
        response = make_market_order_buy(figi=figi_to_buy, quantity=1)
        time.sleep(0.2)
