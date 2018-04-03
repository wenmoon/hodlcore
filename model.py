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

    def __str__(self):
        return 'Mcap: {}, 24h vol: {}, BTC: {}'.format(self.mcap, self.volume_usd_24h, self.bitcoin_percentage_of_market_cap)


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
            token_id = json['id']
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
                token_id, name, symbol, rank, price, price_btc, percent_change_1h, percent_change_24h, percent_change_7d,
                volume_24h, mcap, available_supply, total_supply, max_supply
            )
        except Exception as e:
            return None

    def matches(self, search):
    	search = search.lower()
    	if search in self.id.lower() or search in self.symbol.lower() or search in self.name.lower():
            return True
        return False

    def matches_score(self, search):
        score = 0
        search = search.lower()
        if search == self.id.lower():
            score += 10
        elif search in self.id.lower():
            score += 3

        if search == self.symbol.lower():
            score += 10
        elif search in self.symbol.lower():
            score += 3

        if search == self.name.lower():
            score += 10
        elif search in self.name.lower():
            score += 3

        return score

    @staticmethod
    def is_bitcoin(token_id):
        return token_id.lower() == 'btc'

    def is_bitcoin(self):
        return self.symbol.lower() == 'btc'

    def __str__(self):
        return self.name_str


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


class PeriodicSummary(object):
    def __init__(self, name, now, today, last_week, last_month):
        self.name = name
        self.now = float(now)
        self.last_week = float(last_week)
        self.last_month = float(last_month)

        self.diff_today = now - today
        self.pct_today = 0 if today == 0 else ((now / float(today)) - 1.0) * 100.0

        self.diff_week = now - last_week
        self.pct_week =  0 if last_week == 0 else ((now / float(last_week)) - 1.0) * 100.0

        self.diff_month = now - last_month
        self.pct_month = 0 if last_month == 0 else ((now / float(last_month)) - 1.0) * 100.0

    def __str__(self):
        return 'PeriodicSummary:\n\tName: {}\n\tNumbers (n, lw, lm): {}, {}, {}\n\tDiff (d, w, m): {}, {}, {}\n\tPercent (d, w, m): {}, {}, {}'.format(self.name, self.now, self.last_week, self.last_month, self.diff_today, self.diff_week, self.diff_month, stringformat.percent(self.pct_today), stringformat.percent(self.pct_week), stringformat.percent(self.pct_month))


class OAuthCredentials(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    @classmethod
    def from_json(cls, json):
        try:
            consumer_key = json['consumer_key']
            consumer_secret = json['consumer_secret']
            access_token = json['access_token']
            access_token_secret = json['access_token_secret']
            return cls(consumer_key, consumer_secret, access_token, access_token_secret)
        except Exception:
            return None


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
