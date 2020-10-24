'''
Copyright (C) 2020 Oumayma Zinoun & Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Oumayma Zinoun and Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

from importation import HistoricalData

class markowitzPortfolio:

    #public:

        def __init__ (self, tickers, number_of_data, frequency='1w'):
            self.tickers = tickers
            self.frequency = frequency
            self.historical_data = None
            self.start_date = 
            self.end_date = 

        def load_historical_data (self):
            print ("==> Loading historical data")
            try:
                self.historical_data = HistoricalData (tickers=self.tickers, start_date=self.start_date, frequency=self.frequency).download ()
                print ("==> Data successfully loaded")
            except:
                print ("==> Error importation")
                
        def get_optimal_weights (self, volatility_level):
            optimal_weights = 0
            return optimal_weights

        
