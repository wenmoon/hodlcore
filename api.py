#!/usr/bin/env python
import requests
import json
import model

__endpoint_tickers_all = 'https://api.coinmarketcap.com/v1/ticker/?limit=10000'
__endpoint_token = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'
__endpoint_mcap = 'https://api.coinmarketcap.com/v1/global/'
__endpoint_subreddits = 'https://www.reddit.com/r/{}/about.json'

__headers_useragent = { 'User-agent': 'hodlcore beta' }


def get_mcap():
    mcap_json = requests.get(__endpoint_mcap).json()
    return model.MarketCapitalization(mcap_json)

def get_token(name, balance, currency):
    r_token = requests.get(__endpoint_token.format(name, currency)).json()[0]
    return model.Token(r_token, balance, currency)

def search_token(search):
    r_tokens = requests.get(__endpoint_tickers_all).json()
    for r_token in r_tokens:
        try:
            token = model.Token(r_token)
            if token.matches(search):
                return token
        except:
            return None

def search_tokens(search):
    r_tokens = requests.get(__endpoint_tickers_all).json()
    tokens = []
    for r_token in r_tokens:
        try:
            token = model.Token(r_token)
            if token.matches(search):
                tokens.append(token)
        except:
            pass
    return tokens

def get_portfolio(portfolio_config, currency):
    portfolio = model.Portfolio()
    # get stats for each coin
    for item in portfolio_config:
        token = get_token(item[0], item[1], currency)
        portfolio.add_token(token)
    return portfolio

def get_subreddit(subreddit):
    r_subreddit = requests.get(__endpoint_subreddits.format(subreddit), headers = __headers_useragent).json()['data']
    try:
        return model.Subreddit(r_subreddit)
    except KeyError:
        return None