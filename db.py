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
        self.database_table_cmc_data = 'coinmarketcap_data'

        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1').format(self.database_table_cmc_data)
        except sqlite3.OperationalError:
            self.create_tables(dbc)
        dbc.close()

    def create_tables(self, dbc):
        try:
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         mcap TEXT,
                         volume REAL,
                         bitcoin_percentage_of_market_cap REAL)'''.format(self.database_table_cmc_data))
            dbc.commit()
        except Error as e:
            print(e)

    def insert(self, mcap):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('''INSERT INTO {}
                (mcap, volume, bitcoin_percentage_of_market_cap)
                 VALUES (?, ?, ?)'''.format(self.database_table_cmc_data), (
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
            latest = dbc.execute('SELECT * FROM {} ORDER BY timestamp DESC LIMIT 1'.format(self.database_table_cmc_data)).fetchone()
            return model.MarketCapitalization(float(latest[1]), float(latest[2]), float(latest[3]))
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

    def get_token_ids(self):
        dbc = sqlite3.connect(self.database_file)
        try:
            token_ids = dbc.execute('SELECT id from {} GROUP BY id'.format(self.database_table_cmc_tokens)).fetchall()
            dbc.close()
            return token_ids
        except:
            dbc.close()
            return []


    def get_volumes(self, token_id):
        dbc = sqlite3.connect(db)
        last = dbc.execute(
            'SELECT volume_usd FROM {} WHERE id=? ORDER BY timestamp DESC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
        ).fetchone()

        a_day_ago = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "-1 days") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
        ).fetchone()

        volume_day = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND id=?'.format(database_table_cmc_tokens), (token_id,)
        ).fetchall()

        volume_week = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND id=?'.format(database_table_cmc_tokens), (token_id,)
        ).fetchall()
        volume_month = dbc.execute(
            'SELECT volume_usd FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND id=?'.format(database_table_cmc_tokens), (token_id,)
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
            return None
        return ret

    def get_ranks(self, token_id):
        dbc = sqlite3.connect(db)
        _latest = c.execute(
            'SELECT rank FROM {} WHERE id=? ORDER BY timestamp DESC LIMIT 2', (token,)
        )
        now = _latest.fetchone()
        last = _latest.fetchone()
        today = dbc.execute(
            'SELECT rank FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
        ).fetchone()
        last_week = dbc.execute(
            'SELECT rank FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
        ).fetchone()
        last_month = dbc.execute(
            'SELECT rank FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
        ).fetchone()
        ath = dbc.execute(
            'SELECT rank FROM {} WHERE id=? ORDER BY rank ASC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
        ).fetchone()
        atl = dbc.execute(
            'SELECT rank FROM {} WHERE id=? ORDER BY rank DESC LIMIT 1'.format(database_table_cmc_tokens), (token_id,)
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
            return None
        return ret

    def get_token_mcap_summary(self, token_id):
        dbc = sqlite3.connect(db)
        now = dbc.execute(
            'SELECT market_cap_usd FROM {} WHERE id=? ORDER BY timestamp DESC', (token,)
        ).fetchone()
        today = dbc.execute(
            'SELECT market_cap_usd FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC', (token_id,)
        ).fetchone()
        last_week = dbc.execute(
            'SELECT market_cap_usd FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC', (token_id,)
        ).fetchone()
        last_month = dbc.execute(
            'SELECT market_cap_usd FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND id=? ORDER BY timestamp ASC', (token_id,)
        ).fetchone()
        dbc.close()

        try:
            return model.PeriodicSummary(token_id, now, today, last_week, last_month)
        except:
            return None


#
# Database operations relating to Subscribables, typically Reddit, Twitter, etc where subscribers (and the change thereof) is an interesting metric
#
class SubscribableDB(object):
    def __init__(self, table_name, table_subscribers_name, defaults = []):
        self.database_file = 'data/hodl.db'
        self.database_table_subscribable = table_name
        self.database_table_subscribable_subscribers = table_subscribers_name

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
            dbc.execute('CREATE TABLE {} (name TEXT PRIMARY KEY)'.format(self.database_table_subscribable))
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        name TEXT,
                        subscribers INTEGER)'''.format(self.database_table_subscribable_subscribers))
            dbc.commit()
        except Error as e:
            print(e)

    def get_tracked(self):
        dbc = sqlite3.connect(self.database_file)
        try:
            tracked = dbc.execute('SELECT * FROM {}'.format(self.database_table_subscribable)).fetchall()
            dbc.close()
            return list(map(lambda x: x[0], tracked))
        except Error as e:
            print(e)
        dbc.close()
        return []

    def track(self, subscribable):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('INSERT INTO {} (name) VALUES (?)'.format(self.database_table_subscribable), (subscribable,))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def untrack(sefl, subscribable):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('DELETE FROM {} WHERE name=? LIMIT 1'.format(self.database_table_subscribable), (subscribable,))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def insert(self, subscribable):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('INSERT INTO {} (name, subscribers) VALUES (?, ?)'.format(self.database_table_subscribable_subscribers), (subscribable.name, subscribable.subscribers))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def insert_many(self, subscribables):
        dbc = sqlite3.connect(self.database_file)
        for subscribable in subscribables:
            try:
                dbc.execute('INSERT INTO {} (name, subscribers) VALUES (?, ?)'.format(self.database_table_subscribable_subscribers), (subscribable.name, subscribable.subscribers))
            except Error as e:
                print(e)
        dbc.commit()
        dbc.close()

    def get_subscribers(self, subscribable):
        dbc = sqlite3.connect(self.database_file)
        now = c.execute(
            'SELECT * FROM {} WHERE subscribable=? ORDER BY timestamp DESC'.format(table_subscribers_name), (sr,)
        ).fetchone()
        today = c.execute(
            'SELECT * FROM {} WHERE timestamp BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") AND subscribable=? ORDER BY timestamp ASC'.format(table_subscribers_name), (subscribable.name,)
        ).fetchone()
        last_week = c.execute(
            'SELECT * FROM {} WHERE timestamp BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") AND subscribable=? ORDER BY timestamp ASC'.format(table_subscribers_name), (subscribable.name,)
        ).fetchone()
        last_month = c.execute(
            'SELECT * FROM {} WHERE timestamp BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") AND subscribable=? ORDER BY timestamp ASC'.format(table_subscribers_name), (subscribable.name,)
        ).fetchone()
        dbc.close()

        try:
            return model.PeriodicSummary(subscribable.name, now, today, last_week, last_month)
        except:
            return None

class TwitterDB(SubscribableDB):
    def __init__(self):
        defaults = []
        with open('defaults-twitter.json', 'r') as file:
            defaults = json.load(file)
        super(TwitterDB, self).__init__('twitter', 'twitter_subscribers', defaults)


#
# Database operations relating to Reddit
#
class RedditDB(SubscribableDB):
    def __init__(self):
        defaults = []
        with open('defaults-reddit.json', 'r') as file:
            defaults = json.load(file)
        super(RedditDB, self).__init__('reddit', 'reddit_subscribers', defaults)
