#!/usr/bin/env python3

import yfinance as yf
import argparse
from pprint import pprint
from datetime import datetime

import yaml

def main(ticker, info=None):
    ticker = yf.Ticker(ticker)
    if not info:
        print(ticker.info)
    else:
        print(ticker.info[info])

    symbol = ticker.info["symbol"]
    bid = ticker.info["bid"]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Print targets')
    parser.add_argument('--ticker', required=True)
    parser.add_argument('--info', required=False)

    args = parser.parse_args()
    main(args.ticker, info=args.info)


