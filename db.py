#!/usr/bin/env python

import time
import sqlite3
from sqlite3 import Error
import json

import model

#
# Database operations relating to Market Capitalization
#
class MarketCapitalizationDB(object):
    def __init__(self):
        self.database_file = 'data/hodl.db'
        self.database_table_cmc_global = 'coinmarketcap_global'

        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1').format(self.database_table_cmc_global)
        except sqlite3.OperationalError:
            self.create_tables(dbc)
        dbc.close()

    def create_tables(self, dbc):
        try:
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         mcap TEXT,
                         volume REAL,
                         bitcoin_percentage_of_market_cap REAL)'''.format(self.database_table_cmc_global))
            dbc.commit()
        except Error as e:
            print(e)

    def insert(self, mcap):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('''INSERT INTO {}
                (mcap, volume, bitcoin_percentage_of_market_cap)
                 VALUES (?, ?, ?)'''.format(self.database_table_cmc_global), (
                    mcap.mcap_usd,
                    mcap.volume_usd_24h,
                    mcap.bitcoin_percentage_of_market_cap))
            dbc.commit()
        except KeyError:
            print('Error importing mcap: %s' % mcap)
        dbc.close()

    def get_latest(self):
        dbc = sqlite3.connect(self.database_file)
        dbc.row_factory = sqlite3.Row
        try:
            latest = dbc.execute('SELECT mcap, volume, bitcoin_percentage_of_market_cap FROM {} ORDER BY timestamp DESC LIMIT 1'.format(self.database_table_cmc_global)).fetchone()
            return model.MarketCapitalization(float(latest[0]), float(latest[1]), float(latest[2]))
        except Error as e:
            print(e)
        dbc.close()


#
# Database operations relating to Tokens
#
class TokenDB(object):
    def __init__(self):
        self.database_file = 'data/hodl.db'
        self.database_table_cmc_tokens = 'coinmarketcap_tokens'

        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1').format(self.database_table_cmc_tokens)
        except sqlite3.OperationalError:
            self.create_tables(dbc)
        dbc.close()

    def create_tables(self, dbc):
        try:
            # Create table
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         id TEXT,
                         name TEXT,
                         symbol TEXT,
                         rank INTEGER,
                         price_usd REAL,
                         price_btc REAL,
                         volume_usd REAL,
                         market_cap_usd REAL,
                         available_supply REAL)'''.format(self.database_table_cmc_tokens))
            dbc.commit()
        except Error as e:
            print(e)

    def insert(self, tokens):
        dbc = sqlite3.connect(self.database_file)
        for token in tokens:
            try:
                dbc.execute('''INSERT INTO {}
                    (id, name, symbol, rank, price_usd, price_btc,
                     volume_usd, market_cap_usd, available_supply)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''.format(self.database_table_cmc_tokens), (
                        token.id,
                        token.name,
                        token.symbol,
                        token.rank,
                        token.price,
                        token.price_btc,
                        token.volume_24h,
                        token.mcap,
                        token.available_supply))
            except KeyError as e:
                print(e)
        dbc.commit()
        dbc.close()

    def get_volumes(self, token_id):
        dbc = sqlite3.connect(self.database_file)
        last = dbc.execute(
            'SELECT volume_usd FROM {} WHERE id=? ORDER BY timestamp DESC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()

        a_day_ago = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "-1 days") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()

        volume_day = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND id=?'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchall()

        volume_week = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND id=?'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchall()
        volume_month = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND id=?'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchall()
        dbc.close()

        # Todo, use namedtuple?
        try:
            ret = {
                'last': last[0],
                'yesterday': a_day_ago[0],
                'day_avg': sum([x[0] for x in volume_day]) / len(volume_day),
                'week_avg': sum([x[0] for x in volume_week]) / len(volume_week),
                'month_avg': sum([x[0] for x in volume_month]) / len(volume_month)
            }
        except TypeError:
            print('get_volumes({}) Error: {}'.format(token_id, e))
            return None
        return ret

    def get_ranks(self, token_id):
        dbc = sqlite3.connect(self.database_file)
        _latest = c.execute(
            'SELECT rank FROM {} WHERE id=? ORDER BY timestamp DESC LIMIT 2', (token,)
        )
        now = _latest.fetchone()
        last = _latest.fetchone()
        today = dbc.execute(
            'SELECT rank FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()
        last_week = dbc.execute(
            'SELECT rank FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()
        last_month = dbc.execute(
            'SELECT rank FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()
        ath = dbc.execute(
            'SELECT rank FROM {} WHERE id=? ORDER BY rank ASC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()
        atl = dbc.execute(
            'SELECT rank FROM {} WHERE id=? ORDER BY rank DESC LIMIT 1'.format(self.database_table_cmc_tokens), (token_id,)
        ).fetchone()
        dbc.close()

        try:
            ret = {
                'now': now[0],
                'last': last[0],
                'today': today[0],
                'last_week': last_week[0],
                'last_month': last_month[0],
                'ath': ath[0],
                'atl': atl[0],
                'is_ath': now[0] <= ath[0],
                'is_atl': now[0] >= atl[0]
            }
        except TypeError:
            print('get_ranks({}) Error: {}'.format(token_id, e))
            return None
        return ret

    def __get_metric_summary(self, metric_name, token_id):
        dbc = sqlite3.connect(self.database_file)
        now = dbc.execute(
            'SELECT {metric} FROM {table} WHERE id=? ORDER BY timestamp DESC'.format(table=self.database_table_cmc_tokens, metric=metric_name), (token_id,)
        ).fetchone()
        today = dbc.execute(
            'SELECT {metric} FROM {table} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC'.format(table=self.database_table_cmc_tokens, metric=metric_name), (token_id,)
        ).fetchone()
        last_week = dbc.execute(
            'SELECT {metric} FROM {table} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC'.format(table=self.database_table_cmc_tokens, metric=metric_name), (token_id,)
        ).fetchone()
        last_month = dbc.execute(
            'SELECT {metric} FROM {table} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC'.format(table=self.database_table_cmc_tokens, metric=metric_name), (token_id,)
        ).fetchone()
        dbc.close()

        try:
            return model.PeriodicSummary(token_id, now[0], today[0], last_week[0], last_month[0])
        except TypeError as e:
            print('_get_metric_summary({}, {}) Error: {}'.format(metric_name, token_id, e))
            return None

    def get_prices_btc(self, token_id):
        return self.__get_metric_summary('price_btc', token_id)

    def get_mcaps(self, token_id):
        return self.__get_metric_summary('market_cap_usd', token_id)

#
# Database operations relating to Subscribables, typically Reddit, Twitter, etc where subscribers (and the change thereof) is an interesting metric
#
class SubscribableDB(object):
    def __init__(self, table_name, table_subscribers_name, subscribable_type, defaults = []):
        self.database_file = 'data/hodl.db'
        self.database_table_subscribable = table_name
        self.database_table_subscribable_subscribers = table_subscribers_name
        self.subscribable_type = subscribable_type

        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1'.format(self.database_table_subscribable))
            dbc.execute('SELECT * FROM {} LIMIT 1'.format(self.database_table_subscribable_subscribers))
        except sqlite3.OperationalError:
            self.create_tables(dbc)
            for subscribable in defaults:
                self.track(subscribable)
        dbc.close()

    def create_tables(self, dbc):
        try:
            dbc.execute('CREATE TABLE {} (name TEXT PRIMARY KEY, subscribable_type TEXT)'.format(self.database_table_subscribable))
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        name TEXT,
                        subscribable_type TEXT,
                        subscribers INTEGER)'''.format(self.database_table_subscribable_subscribers))
            dbc.commit()
        except Error as e:
            print(e)

    def get_tracked(self):
        dbc = sqlite3.connect(self.database_file)
        try:
            tracked = dbc.execute('SELECT * FROM {} WHERE subscribable_type=?'.format(self.database_table_subscribable), (self.subscribable_type,)).fetchall()
            dbc.close()
            return list(map(lambda x: x[0], tracked))
        except Error as e:
            print(e)
        dbc.close()
        return []

    def track(self, subscribable):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('INSERT INTO {} (name, subscribable_type) VALUES (?, ?)'.format(self.database_table_subscribable), (subscribable, self.subscribable_type))
        except sqlite3.IntegrityError:
            pass
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def untrack(sefl, subscribable):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('DELETE FROM {} WHERE name=? AND subscribable_type=? LIMIT 1'.format(self.database_table_subscribable), (subscribable, self.subscribable_type))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def insert(self, subscribable):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('INSERT INTO {} (name, subscribable_type, subscribers) VALUES (?, ?, ?)'.format(self.database_table_subscribable_subscribers), (subscribable.name, self.subscribable_type, subscribable.subscribers))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def insert_many(self, subscribables):
        dbc = sqlite3.connect(self.database_file)
        for subscribable in subscribables:
            try:
                dbc.execute('INSERT INTO {} (name, subscribable_type, subscribers) VALUES (?, ?, ?)'.format(self.database_table_subscribable_subscribers), (subscribable.name, self.subscribable_type, subscribable.subscribers))
            except Error as e:
                print(e)
        dbc.commit()
        dbc.close()

    def get_subscribers(self, subscribable):
        dbc = sqlite3.connect(self.database_file)
        now = dbc.execute(
            'SELECT subscribers FROM {} WHERE name=? AND subscribable_type=? ORDER BY timestamp DESC'
            .format(self.database_table_subscribable_subscribers), (subscribable, self.subscribable_type)
        ).fetchone()
        today = dbc.execute(
            'SELECT subscribers FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND name=? AND subscribable_type=? ORDER BY timestamp ASC'
            .format(self.database_table_subscribable_subscribers), (subscribable, self.subscribable_type)
        ).fetchone()
        last_week = dbc.execute(
            'SELECT subscribers FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND name=? AND subscribable_type=? ORDER BY timestamp ASC'
            .format(self.database_table_subscribable_subscribers), (subscribable, self.subscribable_type)
        ).fetchone()
        last_month = dbc.execute(
            'SELECT subscribers FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND name=? AND subscribable_type=? ORDER BY timestamp ASC'
            .format(self.database_table_subscribable_subscribers), (subscribable, self.subscribable_type)
        ).fetchone()
        dbc.close()

        try:
            return model.PeriodicSummary(subscribable, float(now[0]), float(today[0]), float(last_week[0]), float(last_month[0]))
        except TypeError as e:
            print('{} get_subscribers({}) Error: {}'.format(self.subscribable_type, subscribable, e))
            return None


#
# Database operations relating to Twitter
#
class TwitterDB(SubscribableDB):
    def __init__(self):
        defaults = []
        with open('defaults-twitter.json', 'r') as file:
            defaults = json.load(file)
        super(TwitterDB, self).__init__(table_name='twitter', table_subscribers_name='twitter_subscribers', subscribable_type='twitter', defaults=defaults)


#
# Database operations relating to Reddit
#
class RedditDB(SubscribableDB):
    def __init__(self):
        defaults = []
        with open('defaults-reddit.json', 'r') as file:
            defaults = json.load(file)
        super(RedditDB, self).__init__(table_name='reddit', table_subscribers_name='reddit_subscribers', subscribable_type='reddit', defaults=defaults)
