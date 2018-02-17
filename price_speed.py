#!/usr/bin/python

import requests
from statistics import mean


def get_price(currency='BTC', to='USD'):
    """Call cryptocompare API to get currency1-to-currency2 pairs"""
    currencies = 'fsym={0}&tsym={1}'.format(currency, to)

    req = requests.get(  'https://min-api.cryptocompare.com/data/histominute?'
                       + currencies
                       + '&limit=60&aggregate=1&e=CCCAGG' )

    data = req.json()

    return [float(item['close']) for item in data['Data']]


def aggregate(data=[], count=5):
    if count == 1:
        return data
    else:
        return [data[i:i + count] for i in range(0, len(data), count)]

def get_change(items):
    if (len(items) >= 2):
        return ((items[1] - items[0]) / items[0])
    else:
        raise ValueError('Missing item(s) to calculate the change')


aggregated = aggregate(get_price(), count=5)

means = [mean(items) for items in aggregated]

pairs = aggregate(means, count=2)

pairs = [pair for pair in pairs if len(pair) == 2]

changes = [get_change(pair) for pair in pairs]

percent_changes = [round(change * 100, 2) for change in changes]


print(percent_changes)
