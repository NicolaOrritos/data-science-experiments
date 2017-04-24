#!/usr/bin/env python2

import sys
import requests
import sched, time
from matplotlib import pyplot as plot
import pandas as pd


def get_ether_current_prices():
    """Gets the Ether prices from "min-api.cryptocompare.com" as BTC, US Dollars and Euros"""
    req  = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR')
    data = req.json()

    print('{0}, {1}, {2}'.format(data['EUR'], data['USD'], data['BTC']))


def repeat_every(seconds, fn):
    """Repeatdly call "fn" every "seconds" seconds"""
    def wrapper(scheduler):
        try:
            fn()
            scheduler.enter(seconds, 1, wrapper, (scheduler,))
        except:
            print('Error executing function')

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(seconds, 1, wrapper, (scheduler,))
    scheduler.run()

# print('EUR, USD, BTC')
# repeat_every(30, get_ether_current_prices)

def currency_prices_last_n_days(currency = 'ETH', to = 'EUR', days = 14):
    """Get day by day price of a currency in respect to another one,
    using the APIs at "min-api.cryptocompare.com".
    Data are from the last "days" days."""

    currencies = 'fsym={0}&tsym={1}'.format(currency, to)
    days = 'limit={0}'.format(days)

    req  = requests.get(  'https://min-api.cryptocompare.com/data/histoday?'
                        + currencies
                        + '&'
                        + days
                        + '&aggregate=1&e=CCCAGG')

    result = req.json()

    list = [float(day['close']) for day in result['Data']]

    return list

def currency_prices_last_year(currency = 'ETH', to = 'EUR'):
    """Get day by day price of a currency in respect to another one,
    using the APIs at "min-api.cryptocompare.com".
    Data are from the last year."""

    currencies = 'fsym={0}&tsym={1}'.format(currency, to)

    try:
        req  = requests.get(  'https://min-api.cryptocompare.com/data/histoday?'
                            + currencies
                            + '&limit=365&aggregate=1&e=CCCAGG')

        result = req.json()

        list = [float(day['close']) for day in result['Data']]
    except ConnectionError:
        print('Could not connect to "min-api.cryptocompare.com"')
        list = []

    return list

def print_help():
    print('Usage:')
    print('  prices-analysis.py --days <DAYS>')


"""btc_prices = currency_prices_last_year('ETH', 'BTC')
eur_prices = currency_prices_last_year('ETH', 'EUR')
usd_prices = currency_prices_last_year('ETH', 'USD')

# Normalize BTC prices (they are all <0):
btc_prices_norm = [price * 1000 for price in btc_prices]

xs = [x for x in range(len(btc_prices))]

plot.plot(xs, btc_prices_norm, 'b-', label='BTC * 1000')
plot.plot(xs, eur_prices     , 'g-', label='EUR')
plot.plot(xs, usd_prices     , 'r-', label='USD')

plot.title('Ether vs other currencies prices')
plot.xlabel('Days since April, 19 2016')
plot.legend()

plot.show()"""

print(sys.argv)

""" sys.argv[1] MUST be the string "--days" and sys.argv[2] MUST be a non-negative number """

if len(sys.argv) >= 3:
    if sys.argv[1] == '--days':
        days = int(sys.argv[2])

        btc_eur_prices = currency_prices_last_n_days('BTC', 'EUR', days)
        eth_eur_prices = currency_prices_last_n_days('ETH', 'EUR', days)

        btc_eur_prices_norm = [price / 20 for price in btc_eur_prices]

        xs = [x for x in range(len(btc_eur_prices))]

        plot.plot(xs, btc_eur_prices_norm, 'y-', label='BTC / 20')
        plot.plot(xs, eth_eur_prices     , 'b-', label='EUR')

        plot.title('Ether vs Bitcoin prices in respect to Euro')
        plot.xlabel('Last {0} days'.format(days))
        plot.legend()

        plot.show()


        btc_frame = pd.DataFrame(btc_eur_prices)
        eth_frame = pd.DataFrame(eth_eur_prices)

        print('Correlation: {0}'.format(btc_frame.corrwith(eth_frame)[0]))
    else:
        print_help()

else:
    print_help()
