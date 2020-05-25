'''
Copyright (C) 2020 Oumayma Zinoun & Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Oumayma Zinoun and Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import importation

def main ():
    tickers = ['^FCHI', '^DJI']
    data = importation.HistoricalData (tickers=tickers, start_date='23 may 2018', end_date='23 may 2019', frequency='1wk')
    data.download ()
    data.candlesticks (tickers='all')
    data.plot (tickers='all', kind='close')
    data.clear ()

main ()
