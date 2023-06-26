"""
Модуль для работы с заявками.
"""

from account_data import ACCOUNT_ID, TINKOFF_TOKEN
from tinkoff.invest import Client, RequestError, OrderDirection, OrderType, Quotation


def make_market_order_buy(figi, quantity, account_id=ACCOUNT_ID):
    with Client(TINKOFF_TOKEN) as client:
        return client.orders.post_order(
            figi=figi,
            quantity=quantity,
            account_id=account_id,
            direction=OrderDirection.ORDER_DIRECTION_BUY,
            order_type=OrderType.ORDER_TYPE_MARKET
        )


def make_market_order_sell(figi, quantity, account_id=ACCOUNT_ID):
    with Client(TINKOFF_TOKEN) as client:
        return client.orders.post_order(
            figi=figi,
            quantity=quantity,
            account_id=account_id,
            direction=OrderDirection.ORDER_DIRECTION_SELL,
            order_type=OrderType.ORDER_TYPE_MARKET
        )


def make_limit_order_buy(figi, quantity, price, account_id=ACCOUNT_ID):
    with Client(TINKOFF_TOKEN) as client:
        return client.orders.post_order(
            figi=figi,
            quantity=quantity,
            price=price,
            account_id=account_id,
            direction=OrderDirection.ORDER_DIRECTION_BUY,
            order_type=OrderType.ORDER_TYPE_MARKET
        )


def make_limit_order_sell(figi, quantity, price, account_id=ACCOUNT_ID):
    with Client(TINKOFF_TOKEN) as client:
        return client.orders.post_order(
            figi=figi,
            quantity=quantity,
            price=price,
            account_id=account_id,
            direction=OrderDirection.ORDER_DIRECTION_SELL,
            order_type=OrderType.ORDER_TYPE_MARKET
        )


def get_order_state(order_id, account_id=ACCOUNT_ID):
    with Client(TINKOFF_TOKEN) as client:
        return client.orders.get_order_state(
            order_id=order_id,
            account_id=account_id
        )


def get_orders(account_id=ACCOUNT_ID):
    with Client(TINKOFF_TOKEN) as client:
        return client.orders.get_orders(
            account_id=account_id
        )


print(get_order_state(order_id='36799661645'))