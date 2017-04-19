#!/usr/bin/env python2

import requests
import sched, time

print('ETH, EUR, USD, BTC')

def get_prices():
    """Gets the Ether prices from "min-api.cryptocompare.com" as BTC, US Dollars and Euros"""
    req  = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR')
    data = req.json()

    print('1, {0}, {1}, {2}'.format(data['EUR'], data['USD'], data['BTC']))


def repeat_every(seconds, fn):
    def wrapper(scheduler):
        try:
            fn()
            scheduler.enter(seconds, 1, wrapper, (scheduler,))
        except:
            print('Error executing function')

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(seconds, 1, wrapper, (scheduler,))
    scheduler.run()

repeat_every(30, get_prices)
