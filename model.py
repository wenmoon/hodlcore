#!/usr/bin/env python

import stringformat
import datetime


class MarketCapitalization(object):
    def __init__(self, mcap_usd, volume_usd_24h, bitcoin_percentage_of_market_cap):
        self.mcap_usd = mcap_usd
        self.volume_usd_24h = volume_usd_24h
        self.bitcoin_percentage_of_market_cap = bitcoin_percentage_of_market_cap

    @classmethod 
    def from_json(cls, json):
        return cls(json['total_market_cap_usd'], json['total_24h_volume_usd'], json['bitcoin_percentage_of_market_cap'])

class Token(object):
    def __init__(self, id, name, symbol, rank, price, price_btc, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h, mcap, available_supply, total_supply, max_supply, balance = 0, currency = 'usd'):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.rank = rank
        self.price = price
        self.price_btc = price_btc
        self.percent_change_1h = percent_change_1h
        self.percent_change_24h = percent_change_24h
        self.percent_change_7d = percent_change_24h
        self.volume_24h = volume_24h
        self.mcap = mcap
        self.available_supply = available_supply
        self.total_supply = total_supply
        self.max_supply = max_supply

        self.name_str = '{} ({})'.format(self.name, self.symbol)
        self.balance = balance
        self.value = self.price * self.balance
        self.value_btc = self.price_btc * self.balance
        self.url = 'https://coinmarketcap.com/currencies/{}/'.format(self.id)

    @classmethod
    def from_db_tuple(cls, db_tuple):
        try:
            return cls(
                db_tuple[0],
                db_tuple[1],
                db_tuple[2],
                int(db_tuple[3]),
                float(db_tuple[4]),
                float(db_tuple[5]),
                float(db_tuple[6]),
                float(db_tuple[7]),
                float(db_tuple[8]),
                float(db_tuple[9]),
                float(db_tuple[10]),
                float(db_tuple[11]),
                float(db_tuple[12])
            )
        except Exception as e:
            return None

    @classmethod
    def from_json(cls, json, balance = 0, currency = 'usd'):
        try:
            tid = json['id']
            name = json['name']
            symbol = json['symbol']
            rank = int(json['rank'])
            price = float(json['price_{}'.format(currency)])
            price_btc = float(json['price_btc'])
            percent_change_1h = float(json['percent_change_1h'])
            percent_change_24h = float(json['percent_change_24h'])
            percent_change_7d = float(json['percent_change_7d'])
            volume_24h = float(json['24h_volume_{}'.format(currency)])
            mcap = float(json['market_cap_{}'.format(currency)])
            available_supply = float(json['available_supply'])
            total_supply = float(json['total_supply'])
            max_supply = float(json['total_supply'])
            return cls(
                tid, name, symbol, rank, price, price_btc, percent_change_1h, percent_change_24h, percent_change_7d, 
                volume_24h, mcap, available_supply, total_supply, max_supply
            )
        except Exception as e:
            return None

    def matches(self, search):
    	search_ci = search.lower()
    	if search_ci in self.id.lower() or search_ci in self.symbol.lower() or search_ci in self.name.lower():
            return True
        return False

    @staticmethod
    def is_bitcoin(token_id):
        return token_id.lower() == 'btc'

    def is_bitcoin(self):
        return self.symbol.lower() == 'btc'

    def __str__():
        return self.name_str

    
class Portfolio(object):
    def __init__(self):
        self.tokens = []
        self.value = 0
        self.value_btc = 0

    def add_tokens(self, token):
        self.tokens.append(token)
        self.value += token.value
        self.value_btc += token.value_btc

    def remove_token(self, token):
        self.tokens.remove(token)
        self.value -= token.value
        self.value_btc -= token.value_btc

    def __str__():
        return self.name_str


class Subscribable(object):
    def __init__(self, name, subscribers, url):
        self.name = name
        self.subscribers = subscribers
        self.url = url


class PeriodicSummary(object):
    def __init__(self, name, now, today, last_week, last_month):
        self.name = name
        self.now = now
        self.diff_today = now - today
        self.pct_today = 0 if today == 0 else ((now / today) - 1) * 100
        self.diff_week = now - last_week
        self.pct_week =  0 if last_week == 0 else ((now / last_week) - 1) * 100
        self.diff_month = now - last_month
        self.pct_month = 0 if last_month == 0 else ((now / last_month) - 1) * 100

    def __str__(self):
        return 'PeriodicSummary:\n\tName: {}\n\tDiff (d, w, m): {}, {}, {}\n\tPercent (d, w, m): {}, {}, {}'.format(self.name, self.diff_today, self.diff_week, self.diff_month, stringformat.percent(self.pct_today), stringformat.percent(self.pct_week), stringformat.percent(self.pct_month))


class OAuthCredentials(object):
    def __init__(self, json):
        self.consumer_key = json['consumer_key']
        self.consumer_secret = json['consumer_secret']
        self.access_token = json['access_token']
        self.access_token_secret = json['access_token_secret']


class Event(object):
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end        
        self.when = self.start - datetime.datetime.now()
        self.finished = True if datetime.datetime.now() > self.end else False
        self.ongoing = True if self.when.days < 0 else False
        self.today = True if self.when.days == 0 else False
        self.upcoming = True if self.when.days > 0 else False
