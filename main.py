import datetime
from datetime import datetime, timedelta
from tinkoff.invest import Client, CandleInterval, HistoricCandle
from pandas import DataFrame


def main():
    with Client(TOKEN) as client:
        r = client.market_data.get_candles(
            figi='BBG00F9XX7H4',
            from_=datetime.now() - timedelta(hours=4),
            to=datetime.now(),
            interval=CandleInterval.C
        )
    df = create_df(r.candles)
    df['ema'] = ema_indicator(close=df['close'], window=9)
    print(df[['time', 'close', 'ema']].tail(10))
    print(df.close.iloc[-1])







if __name__ == '__main__':
    main()
