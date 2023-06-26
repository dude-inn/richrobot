"""
Модуль для настройки логов, параметров стратегий.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'telegram_bot_logger.log')


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=20000000,
    backupCount=2,
)
formatter = logging.Formatter(
    '%(lineno)s - %(levelname)s - %(message)s - %(funcName)s - %(asctime)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


STOCK_FEE = 0.0005
"""
Комиссия при покупке или продаже акций.
"""

CURRENCY_FEE = 0.005
"""
Комиссия при покупке или продаже валюты.
"""

COUNT_OF_OPEN_POSITION = 5
"""
Максимальное количество открытых позиций.
"""

START_TRADING_TIME = '7:00'
"""
Время начала основной сессии Московской биржи (UTC).
"""

FINISH_TRADING_TIME = '15:30'
"""
Время окончания основной сессии Московской биржи (UTC).
"""

UT_BOT_SENSITIVITY = 1
UT_BOT_ATR_PERIOD = 10
"""
UT Bot Parameters.
"""

MACD_SLOW = 26
MACD_FAST = 12
MACD_INDICATOR = 9
"""
MACD Parameters.
"""

SLEEP_TIME_IF_BUY_LIST_IS_EMPTY = 3
