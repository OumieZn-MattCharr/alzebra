'''
Copyright (C) 2020 Oumayma Zinoun & Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Oumayma Zinoun and Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import datetime
import json
import logging as lg
import os

from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from urllib.request import urlopen
from requests import get
import pandas as pd

#test

lg.basicConfig (level=lg.WARNING)

SITE = 'https://uk.finance.yahoo.com/quote/'
HIST = '/history?'
P1 = 'period1='
P2 = 'period2='
INT = 'interval='
FREQ = 'frequency='
ADD = 'filter=history'

INITIAL_DATE = datetime.datetime (year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
DEFAULT_FORMAT = '%d %b %Y'

class HistoricalData:

    #public:

        TODAY = datetime.datetime.today ().strftime (DEFAULT_FORMAT)
        DEFAULT_START_DATE = (datetime.datetime.today () - datetime.timedelta (days=252)).strftime (DEFAULT_FORMAT)
        
        def __init__ (self, tickers=['^FCHI'], start_date=DEFAULT_START_DATE, end_date=TODAY, frequency='1d'):
            '''
                frequency = '1d', '1wk', '1mo'
                start_date, end_date = '%d %b %Y'
            '''
            self.tickers = tickers
            self.frequency = frequency
            self.start_date = start_date
            self.end_date = end_date

        def download (self):
            print ("==> Downloading historical data")
            for ticker in self.tickers:
                print ("==> Downloading historical data for ", ticker)
                try:
                    historical_data_ticker = extract_data (ticker, self.start_date, self.end_date, self.frequency)
                    file_name = get_file_name (ticker, self.start_date, self.end_date, self.frequency)
                    with open (file=file_name, mode='w') as file: json.dump (historical_data_ticker, file)
                    print ("==> Historical data for ", ticker, "was succesfully imported")
                except:
                    print ("==> Importation error for ", ticker)
            return self

        def clear (self):
            os.system ('cd data && rm -rf *')

        def candlesticks (self, tickers='all'):
            '''
                tickers = 'all' or tickers
            '''
            if tickers == 'all': tickers = self.tickers
            for ticker in tickers: 
                file_name = get_file_name (ticker, self.start_date, self.end_date, self.frequency)
                plt.figure ()
                plt.title (ticker + '-' + self.start_date + '-' + self.end_date + '-' + self.frequency)
                plt.xlabel ('dates')
                plt.ylabel ('data')
                plt.xticks (rotation=90)
                with open (file=file_name, mode='r') as file:
                    data = json.load (file)
                    for feature in data [::-1]:
                        date, data = feature.values ()
                        begin, high, low, end, _, _ = data.values ()
                        plt.scatter (date, begin, marker='.', color='black')
                        plt.scatter (date, end, marker='.', color='black')
                        try:
                            plt.plot ([date, date], [low, high], color='green' if begin < end else 'red')
                        except TypeError: pass
                plt.show ()

        def plot (self, tickers='all', kind='close'):
            '''
                tickers = 'all' or tickers
            '''
            if tickers == 'all': tickers = self.tickers
            for ticker in tickers: 
                plt.figure ()
                plt.xticks (rotation=90)
                plt.title (self.start_date + '-' + self.end_date + '-' + self.frequency)
                plt.xlabel ('dates')
                plt.ylabel ('data')
                dates = []; values = []
                file_name = get_file_name (ticker, self.start_date, self.end_date, self.frequency)
                with open (file=file_name, mode='r') as file:
                    data = json.load (file)
                    for feature in data [::-1]:
                        date, data = feature.values ()
                        args = list (data.values ())
                        value = get_value (args, kind)
                        dates.append (date)
                        values.append (value)
                    plt.plot (dates, values, color='black')
                    if kind == 'var': plt.axhline (0, color='grey', linestyle="--")
                    plt.show ()
                        
#toolkit:

def get_value (args, kind):
    if kind == 'open': return args [0]
    elif kind == 'high': return args [1]
    elif kind == 'low': return args [2]
    elif kind == 'close': return args [3]
    elif kind == 'vol': return args [4]
    elif kind == 'var': return args [5]
    else: print ('Cannot find kind')

def get_file_name (ticker, start_date, end_date, frequency):
    formatted_start_date_ = start_date.replace (' ', '_')
    formatted_end_date_ = end_date.replace (' ', '_')
    return 'data/' + ticker + '-' + formatted_start_date_ + '-' + formatted_end_date_ + '-' + frequency + '.json'

def extract_data (ticker, start_date, end_date, frequency):
    start_date_timestamp = from_date_to_timestamp (start_date)
    end_date_timestamp = from_date_to_timestamp (end_date)
    if end_date_timestamp > start_date_timestamp:
        start_date_period = from_timestamp_to_period (start_date_timestamp)
        end_date_period = from_timestamp_to_period (end_date_timestamp)
        results = html_parser (ticker, start_date_period, end_date_period, frequency)
        series, end_date = get_serie (results)
        extracted_data = extract_data (ticker, start_date, end_date, frequency)
        return series + extracted_data
    else: return []

def from_date_to_timestamp (date, initial_date=INITIAL_DATE):
    date_datetime = datetime.datetime.strptime (date, DEFAULT_FORMAT)
    delta = date_datetime - initial_date
    timestamp = delta.total_seconds ()
    return timestamp

def from_timestamp_to_period (date):
    return str (int (date))

def get_url (ticker, period1, period2, frequency):
    return SITE + ticker + HIST + P1 + period1 + '&' + P2 + period2 + '&' + INT + frequency + '&' + ADD + '&' + FREQ + frequency

def html_parser (ticker, start_date, end_date, frequency):
    url = get_url (ticker, start_date, end_date, frequency)
    page = get (url).text
    soup = BeautifulSoup (page, 'html.parser')
    table = soup.find ('table', attrs={'class' : 'W(100%) M(0)'})
    results = table.find_all ('tr')
    return results

def get_index (data, index):
    try: return float (data [index].find ('span').getText ().replace (',', ''))
    except: return None

def get_var (price1, price2):
    try: return 100 * (price2 / price1 - 1)
    except ZeroDivisionError: return None
    except TypeError: return None

def get_parameters (date, data, close0):
    open = get_index (data, 1)
    high = get_index (data, 2)
    low = get_index (data, 3)
    close = get_index (data, 4)
    vol = get_index (data, 6) 
    var = get_var (close0, close)
    return {'open' : open, 'high' : high, 'low' : low, 'close' : close, 'vol' : vol, 'var' : var}, close

def get_serie (results):
    series = list ()
    close0 = 0
    for result in results:
        data = result.find_all ('td')
        if len (data) < 7: continue
        date = data [0].find ('span').getText () 
        parameters, close0 = get_parameters (date, data, close0)
        serie = {'date' : date, 'data' : parameters}
        if parameters != None: series.append (serie)
    return series, date