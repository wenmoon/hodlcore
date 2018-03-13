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

    def summary(self):
        s = '*Global data {}:*\n'.format(stringformat.emoji('charts'))
        s += '*Total Market Cap (USD):* ${}\n'.format(stringformat.large_number(self.mcap_usd))
        s += '*Total 24h Volume (USD):* ${}\n'.format(stringformat.large_number(self.volume_usd_24h))
        s += '*BTC Dominance:* {}'.format(stringformat.percent(self.bitcoin_percentage_of_market_cap, emo=False))
        return s


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
        self.rank = json['rank']
        self.price = float(json['price_{}'.format(currency)])
        self.price_btc = float(json['price_btc'])
        self.percent_change_1h = float(json['percent_change_1h'])
        self.percent_change_24h = float(json['percent_change_24h'])
        self.percent_change_7d = float(json['percent_change_7d'])
        self.volume_24h = json['24h_volume_{}'.format(currency)]
        self.mcap = json['market_cap_{}'.format(currency)]
        self.available_supply = json['available_supply']
        self.total_supply = json['total_supply']
        self.max_supply = json['total_supply']
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

    def summary(self):
        s = '*Rank:* #{}\n'.format(self.rank)
        s += '*Price (USD):* ${}\n'.format(self.price)
        s += '*Price (BTC):* {}\n'.format(self.price_btc)
        s += '*24h Volume:* {}\n'.format(stringformat.large_number(self.volume_24h))
        s += '*Market Cap:* {}\n'.format(stringformat.large_number(self.mcap))
        s += '*Avail. Supply:* {}\n'.format(stringformat.large_number(self.available_supply))
        s += '*Total Supply:* {}\n'.format(stringformat.large_number(self.total_supply))
        s += '*Max Supply:* {}\n'.format(stringformat.large_number(self.max_supply))
        s += '*Change (1h):* {}\n'.format(stringformat.percent(self.percent_change_1h, emo=True))
        s += '*Change (24h):* {}\n'.format(stringformat.percent(self.percent_change_24h, emo=True))
        s += '*Change (7d):* {}'.format(stringformat.percent(self.percent_change_7d, emo=True))
        return s

    def compared_summary(self, other_token):
        s = '*{} {} {}*:\n'.format(self.name, stringformat.emojis['vs'], other_token.name)
        s += '*Rank:* #{} vs #{}\n'.format(self.rank, other_token.rank)
        s += '*Price (USD):* ${} vs ${}\n'.format(self.price, other_token.price)
        s += '*Price (BTC):* {} vs {}\n'.format(self.price_btc, other_token.price_btc)
        s += '*24h Volume:* {} vs {}\n'.format(stringformat.large_number(self.volume_usd), stringformat.large_number(other_token.volume_usd))
        s += '*Market Cap:* {} vs {}\n'.format(stringformat.large_number(self.mcap), stringformat.large_number(other_token.mcap))
        s += '*Avail. Supply:* {} vs {}\n'.format(stringformat.large_number(self.available_supply), stringformat.large_number(other_token.available_supply))
        s += '*Total Supply:* {} vs {}\n'.format(stringformat.large_number(self.total_supply), stringformat.large_number(other_token.total_supply))
        s += '*Max Supply:* {} vs {}\n'.format(stringformat.large_number(self.max_supply), stringformat.large_number(other_token.max_supply))
        s += '*Change (1h):* {} vs {}\n'.format(stringformat.percent(self.percent_change_1h, emo=True), stringformat.percent(other_token.percent_change_1h, emo=True))
        s += '*Change (24h):* {} vs {}\n'.format(stringformat.percent(self.percent_change_24h, emo=True), stringformat.percent(other_token.percent_change_24h, emo=True))
        s += '*Change (7d):* {} vs {}\n'.format(stringformat.percent(self.percent_change_7d, emo=True), stringformat.percent(other_token.percent_change_7d, emo=True))
        mcap_factor = self.mcap / other_token.mcap
        mcap_price = mcap_factor * other_token.price_usd
        vol_factor = self.volume_24h / other_token.volume_24h
        s += '*{} has {:.2f}x the 24h volume of {}.*\n'.format(self.name, vol_factor, other_token.name)
        s += '*{} has {:.2f}x the 24h volume of {}.*\n'.format(self.name, vol_factor, other_token.name)
        s += '*If {} had the market cap of {}, the USD price would be: ${} ({:.1f}x)*'.format(self.name, other_token.name, mcap_price, mcap_factor)
        return s


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
