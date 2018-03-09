#!/usr/bin/env python
from collections import namedtuple

class MarketCapitalization(object):
    def __init__(self, json):
        self.mcap_usd = json['total_market_cap_usd']
        self.volume_usd_24h = json['total_24h_volume_usd']
        self.bitcoin_percentage_of_market_cap = json['bitcoin_percentage_of_market_cap']


class Token(object):
    # @classmethod
    # def from_db_tuple(token,db_tuple):
    #     currency = 'usd'
    #     balance = 0
    #     self.id = db_tuple[0]
    #     self.name = db_tuple[1]
    #     self.symbol = db_tuple[2]
    #     self.rank = db_tuple[3]
    #     self.price = float(db_tuple[4])
    #     self.price_btc = float(db_tuple[5])
    #     self.percent_change_1h = float(db_tuple[6])
    #     self.percent_change_24h = float(db_tuple[7])
    #     self.percent_change_7d = float(db_tuple[8])
    #     self.volume_24h = db_tuple[9]
    #     self.market_cap = db_tuple[10]
    #     self.available_supply = db_tuple[11]
    #     self.total_supply = db_tuple[12]
    #     #
    #     self.name_str = '{} ({})'.format(self.name, self.symbol)
    #     self.balance = balance
    #     self.value = self.price * self.balance
    #     self.value_btc = self.price_btc * self.balance
    #     self.url = 'https://coinmarketcap.com/currencies/{}/'.format(self.id)

    def __init__(self, json, balance = 0, currency = 'usd'):
        self.id = json['id']
        self.name = json['name']
        self.symbol = json['symbol']
        self.rank = json['rank']
        self.price = float(json['price_{}'.format(currency)])
        self.price_btc = float(json['price_btc'])
        self.percent_change_1h = float(json['percent_change_1h'])
        self.percent_change_24h = float(json['percent_change_24h'])
        self.percent_change_7d = float(json['percent_change_7d'])
        self.volume_24h = json['24h_volume_{}'.format(currency)]
        self.market_cap = json['market_cap_{}'.format(currency)]
        self.available_supply = json['available_supply']
        self.total_supply = json['total_supply']
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

class OAuthCredentials(object):
    def __init__(self, json):
        self.consumer_key = json['consumer_key']
        self.consumer_secret = json['consumer_secret']
        self.access_token = json['access_token']
        self.access_token_secret = json['access_token_secret']
