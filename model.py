#!/usr/bin/env python

import stringformat

class MarketCapitalization(object):
    def __init__(self, mcap_usd, volume_usd_24h, bitcoin_percentage_of_market_cap):
        self.mcap_usd = mcap_usd
        self.volume_usd_24h = volume_usd_24h
        self.bitcoin_percentage_of_market_cap = bitcoin_percentage_of_market_cap

    @classmethod
    def from_json(mcap, json):
        return mcap(json['total_market_cap_usd'], json['total_24h_volume_usd'], json['bitcoin_percentage_of_market_cap'])


class Token(object):
    # @classmethod
    # def from_db_tuple(token, db_tuple):
    #     currency = 'usd'
    #     balance = 0
    #     return token(
    #         db_tuple[0],
    #         db_tuple[1],
    #         db_tuple[2],
    #         db_tuple[3],
    #         float(db_tuple[4]),
    #         float(db_tuple[5]),
    #         float(db_tuple[6]),
    #         float(db_tuple[7]),
    #         float(db_tuple[8]),
    #         db_tuple[9],
    #         db_tuple[10],
    #         db_tuple[11],
    #         db_tuple[12],
    #         '{} ({})'.format(self.name, self.symbol),
    #         balance,
    #         self.price * self.balance,
    #         self.price_btc * self.balance,
    #         'https://coinmarketcap.com/currencies/{}/'.format(self.id)
    #     )

    def __init__(self, json, balance = 0, currency = 'usd'):
        self.id = json['id']
        self.name = json['name']
        self.symbol = json['symbol']
        self.rank = int(json['rank'])
        self.price = float(json['price_{}'.format(currency)])
        self.price_btc = float(json['price_btc'])
        self.percent_change_1h = float(json['percent_change_1h'])
        self.percent_change_24h = float(json['percent_change_24h'])
        self.percent_change_7d = float(json['percent_change_7d'])
        self.volume_24h = float(json['24h_volume_{}'.format(currency)])
        self.mcap = float(json['market_cap_{}'.format(currency)])
        self.available_supply = float(json['available_supply'])
        self.total_supply = float(json['total_supply'])
        self.max_supply = float(json['total_supply'])
        #
        self.name_str = '{} ({})'.format(self.name, self.symbol)
        self.balance = balance
        self.value = self.price * self.balance
        self.value_btc = self.price_btc * self.balance
        self.url = 'https://coinmarketcap.com/currencies/{}/'.format(self.id)

    def matches(self, search):
    	search_ci = search.lower()
    	if search_ci in self.id.lower() or search_ci in self.symbol.lower() or search_ci in self.name.lower():
            return True
        return False

    
class Portfolio(object):
    def __init__(self):
        self.tokens = []
        self.value = 0
        self.value_btc = 0

    def add_token(self, token):
        self.tokens.append(token)
        self.value += token.value
        self.value_btc += token.value_btc

    def remove_token(self, token):
        self.tokens.remove(token)
        self.value -= token.value
        self.value_btc -= token.value_btc


class Subscribable(object):
    def __init__(self, name, subscribers, url):
        self.name = name
        self.subscribers = subscribers
        self.url = url

    @classmethod
    def from_json(sub, json):
        return sub(json['display_name'], json['subscribers'], json['url'])


class PeriodicSummary(object):
    def __init__(self, name, now, today, week, month):
        self.name = names
        self.now = now
        self.diff_today = now - today
        self.pct_today = ((now / today) - 1) * 100
        self.diff_week = now - last_week
        self.pct_week =  ((now / last_week) - 1) * 100
        self.diff_month = now - last_month
        self.pct_month = ((now / last_month) - 1) * 100


class OAuthCredentials(object):
    def __init__(self, json):
        self.consumer_key = json['consumer_key']
        self.consumer_secret = json['consumer_secret']
        self.access_token = json['access_token']
        self.access_token_secret = json['access_token_secret']
