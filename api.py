#!/usr/bin/env python
import requests
import json
import model

__endpoint_tokens_all = 'https://api.coinmarketcap.com/v1/ticker/?limit=10000'
__endpoint_tokens_limit = 'https://api.coinmarketcap.com/v1/ticker/?limit={}'
__endpoint_token = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'
__endpoint_mcap = 'https://api.coinmarketcap.com/v1/global/'
__endpoint_subreddits = 'https://www.reddit.com/r/{}/about.json'

__headers_reddit = { 'User-agent': 'hodlmybot beta' }


def get_mcap():
    mcap_json = requests.get(__endpoint_mcap).json()
    return model.MarketCapitalization(mcap_json)

def get_token(name, balance, currency):
    r_token = requests.get(__endpoint_token.format(name, currency)).json()[0]
    return model.Token(r_token, balance, currency)

def get_top_tokens(limit):
    r_token = requests.get(__endpoint_tokens_limit.format(limit)).json()[0]
    tokens = []
    for r_token in r_tokens:
        try:
            tokens.append(model.Token(r_token))
        except:
            pass
    return tokens

def search_token(search):
    r_tokens = requests.get(__endpoint_tickers_all).json()
    for r_token in r_tokens:
        try:
            token = model.Token(r_token)
            if token.matches(search):
                return token
        except:
            return None

def search_tokens(search, limit = 100):
    r_tokens = requests.get(__endpoint_tokens_all).json()
    tokens = []
    for r_token in r_tokens:
        try:
            token = model.Token(r_token)
            if token.matches(search):
                tokens.append(token)
            if len(tokens) >= limit:
                break
        except:
            pass
    return tokens

def get_portfolio(portfolio_config, currency):
    portfolio = model.Portfolio()
    for item in portfolio_config:
        token = get_token(item[0], item[1], currency)
        portfolio.add_token(token)
    return portfolio

def get_subreddit(subreddit):
    r_subreddit = requests.get(__endpoint_subreddits.format(subreddit), headers = __headers_reddit).json()['data']
    try:
        return model.Subreddit(r_subreddit)
    except KeyError:
        return None