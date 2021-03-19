#!/usr/bin/env python3

import yfinance as yf
import argparse
from pprint import pprint
from datetime import datetime

import yaml

def main(ticker_filter=None, account_filter=None):
    with open("holdings.yml", 'r') as stream:
        try:
            account_holdings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    for account, holdings in account_holdings.items():
        if account_filter and account_filter.lower() != account.lower():
            continue
        print(account + "\n")
        symbols = [holding["symbol"] for holding in holdings]
        for holding in holdings:
            if ticker_filter and ticker_filter.lower() != holding["symbol"].lower():
                continue
            ticker = yf.Ticker(holding["symbol"])
            symbol = ticker.info["symbol"]
            cost = holding["cost"]
            shares = holding["shares"]
            bid = ticker.info["bid"]

            value = bid * shares
            pl = value - cost
            shares_in_contract = 100
            contracts = int(shares/shares_in_contract)
            optionable_value = contracts * shares_in_contract * bid
            avg_price_per_share = cost / shares

            target_percentages = [7, 10, 20]
            target_percentages = range(5, 25, 5)
            print(f"{symbol} cost: {cost} value: {round(value, 2)} p/l: {round(pl, 2)} contracts: {contracts} avg pps: {round(avg_price_per_share, 3)}\n")

            periods = {"year": 1, "month": 12, "week": 52}

            columns = ["percent"] + [label for label, _ in periods.items()]
            template = " ".join(["{: >20}"] * len(columns))
            print(template.format(*columns))
            for target_percentage in target_percentages:
                target_value = target_percentage / 100 * optionable_value
                period_target_values = []
                for label, period in periods.items():
                    period_target_values.append(round(target_value/period, 2))
                row = [f"{target_percentage}%"] + period_target_values
                print(template.format(*row))
            print("\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Print targets')
    parser.add_argument('--ticker', required=False)
    parser.add_argument('--account', required=False)

    args = parser.parse_args()
    main(ticker_filter=args.ticker, account_filter=args.account)


