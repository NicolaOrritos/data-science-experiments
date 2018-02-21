#!/usr/bin/python

import requests
from statistics import mean


def get_prices(currency='BTC', to='USD', samples_count=60):
    """Call cryptocompare API to get currency1-to-currency2 pairs"""
    currencies = 'fsym={0}&tsym={1}'.format(currency, to)

    req = requests.get(  'https://min-api.cryptocompare.com/data/histominute?'
                       + currencies
                       + '&limit='
                       + str(samples_count)
                       + '&aggregate=1&e=CCCAGG' )

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


currency = 'BTC'
fiat = 'USD'
minutes_interval = 15
samples = 6000


prices = get_prices(currency=currency, to=fiat, samples_count=samples)

aggregated = aggregate(prices, count=minutes_interval)

means = [mean(items) for items in aggregated]

pairs = aggregate(means, count=2)

pairs = [pair for pair in pairs if len(pair) == 2]

changes = [get_change(pair) for pair in pairs]

# Percent-per-minute change:
changes_speed = [abs(change / minutes_interval) for change in changes]


from matplotlib import pyplot as plot
from two_scales import two_scales

price_samples = [means[index] for index in range(1, len(means), 2)]

xs = range(len(changes_speed))

# Create axes
_, ax = plot.subplots()

plot.xlabel('Last {0} samples'.format(len(price_samples)))

ax1, ax2 = two_scales(ax, xs, changes_speed, price_samples, 'r', 'b',
                      'Prices change speed (percent-points-per-minute)',
                      'Price ({0})'.format(fiat))

ax1.legend(loc=2)
ax2.legend()

plot.title('Bitcoin prices change speed - {0} minutes intervals'.format(minutes_interval))
plot.show()
