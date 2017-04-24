#!/usr/bin/env python2

import sys
import requests
from matplotlib import pyplot as plot
import pandas as pd


def currency_data_last_n_days(currency = 'ETH', to = 'EUR', days = 14):
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

    return result['Data']


def pick(stats, data):
    return map( lambda day_data: {stat: day_data[stat] for stat in stats}, data)


def print_help():
    print('Usage:')
    print('  currency-data.py --currency [BTC | ETH] --days <DAYS> --stats <STATISTIC_1_NAME>,<STATISTIC_2_NAME>,etc')


""" sys.argv[1] MUST be the string "--currency" and sys.argv[2] MUST be either "BTC" or "ETH" """
""" sys.argv[3] MUST be the string "--days" and sys.argv[4] MUST be a non-negative number """

if len(sys.argv) == 7:
    if sys.argv[1] == '--currency' and (sys.argv[2] == 'BTC' or sys.argv[2] == 'ETH'):
        currency = sys.argv[2]

        if sys.argv[3] == '--days':
            days = int(sys.argv[4])

            if sys.argv[5] == '--stats':
                stats = sys.argv[6].split(',')

                if len(stats) == 2:
                    result = pick(  stats
                                  , currency_data_last_n_days(currency, to='EUR', days=days) )
                    print(result)

                    xs = [item[stats[0]] for item in result]
                    ys = [item[stats[1]] for item in result]

                    plot.scatter(xs, ys)
                    plot.title('{0} vs {1}'.format(stats[0], stats[1]))
                    plot.xlabel(stats[0])
                    plot.ylabel(stats[1])
                    plot.show()
                else:
                    print_help()
            else:
                print_help()

        else:
            print_help()
    else:
        print_help()

else:
    print_help()
