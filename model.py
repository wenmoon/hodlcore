#!/usr/bin/env python

class MarketCapitalization(object):
    def __init__(self, json):
        self.mcap_usd = json['total_market_cap_usd']
        self.volume_usd_24h = json['total_24h_volume_usd']

class Token(object):
    def __init__(self, json, balance = 0, currency = 'usd'):
        self.id = json['id']
        self.name = json['name']
        self.symbol = json['symbol']
        self.name_str = '%s (%s)' % (self.name, self.symbol)
        self.rank = json['rank']
        self.price = float(json['price_%s' % currency])
        self.price_btc = float(json['price_btc'])
        self.percent_change_1h = float(json['percent_change_1h'])
        self.percent_change_24h = float(json['percent_change_24h'])
        self.percent_change_7d = float(json['percent_change_7d'])
        self.volume_24h = json['24h_volume_%s' % currency]
        self.market_cap = json['market_cap_%s' % currency]
        self.available_supply = json['available_supply']
        self.total_supply = json['total_supply']
        self.balance = balance
        self.value = self.price * self.balance
        self.value_btc = self.price_btc * self.balance

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

class Subreddit(object):
    def __init__(self, name, subscribers, url):
        self.name = name
        self.subscribers = subscribers
        self.url = url

    def __init__(self, json):
        self.name = json['display_name']
        self.subscribers = json['subscribers']
        self.url = json['url']  
