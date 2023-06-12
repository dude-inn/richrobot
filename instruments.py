from tinkoff.invest import Client, InstrumentStatus, SharesResponse, InstrumentIdType
from tinkoff.invest.services import InstrumentsService, MarketDataService
from tinkoff.invest import Client, CandleInterval, HistoricCandle
from pandas import DataFrame

from account_data import TOKEN

TICKER = 'AFLT'


def getfigi(ticker):
    """
    Функция возвращает figi акции по ее тикеру.
    :param ticker:
    :return:
    """
    with Client(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        r = DataFrame(
            instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE).instruments,
            columns=['name', 'figi', 'ticker', 'class_code']
        )
    r = r[r['ticker'] == ticker]['figi'].iloc[0]
    return r


def cast_money(v) -> float:
    """
    Функция для преобразования Quotation в int
    :param v:
    :return: float
    """
    return v.units + v.nano / 1e9


def create_df(candles: [HistoricCandle]):
    return DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])


def getinstruments_of_TQBR():
    """
    Функция записывающая в файл stocks_data.
    Информацию по акциям (имя, тикер, figi), торгующихся
    на московской бирже
    :return: None
    """
    with Client(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        r = DataFrame(
            instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments,
            columns=['ticker', 'name', 'figi', 'class_code']
        )
    r = r[r['class_code'] == 'TQBR']
    json_file = r.to_json(orient='records')
    with open('stocks_data.json', 'w', encoding='utf8', newline='') as f:
        f.write(json_file)

getinstruments_of_TQBR()
