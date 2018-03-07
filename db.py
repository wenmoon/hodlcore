#!/usr/bin/env python
import sqlite3
from sqlite3 import Error
import time

class MarketCapitalizationDB(object):
    def __init__(self):
        self.database_file = 'data/hodl.db'
        self.database_table_cmc_mcap = 'coinmarketcap_mcap'

        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1').format(self.database_table_cmc_mcap)
        except sqlite3.OperationalError:
            self.create_tables(dbc)
        dbc.close()

    def create_tables(self, dbc):
        try:
            # Create table
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         mcap TEXT,
                         volume REAL)'''.format(self.database_table_cmc_mcap))
            dbc.commit()
        except Error as e:
            print(e)

    def insert(self, mcap):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('''INSERT INTO {}
                (mcap, volume) 
                 VALUES (?, ?)'''.format(self.database_table_cmc_mcap), (
                    mcap.mcap_usd,
                    mcap.volume_usd_24h))
        except KeyError:
            print('Error importing mcap: %s' % mcap)
        dbc.commit()
        dbc.close()


class TokensDB(object):
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
                        token.market_cap,
                        token.available_supply))
            except KeyError as e:
                print(e)
        dbc.commit()
        dbc.close()


class RedditDB(object):
    def __init__(self):
        self.database_file = 'data/hodl.db'
        self.database_table_subreddit = 'subreddit'
        self.database_table_subreddit_followers = 'subreddit_followers'

        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1'.format(self.database_table_subreddit))
            dbc.execute('SELECT * FROM {} LIMIT 1'.format(self.database_table_subreddit_followers))
        except sqlite3.OperationalError:
            self.create_tables(dbc)
            default_subreddits = [
                'bitcoin',
                'ethereum',
                'litecoin',
                'NEO',
                'nebulas',
                'Monero',
                'Ripple',
                'IOTA',
                'nanocurrency',
                'vertcoin',
                'HEROcoin',
                'XRPTalk',
                'Electroneum',
                'dogecoin',
                'reddCoin',
                'Lisk',
                'siacoin',
                'steem',
                'komodoplatform',
                'SaltCoin',
                'gnosisPM',
                'Quantstamp',
                'COSS',
                'CossIO',
            ]
            for subreddit in default_subreddits:
                self.track(subreddit)
        dbc.close()

    def create_tables(self, dbc):
        try:
            dbc.execute('CREATE TABLE {} (name TEXT PRIMARY KEY)'.format(self.database_table_subreddit))
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        name TEXT,
                        subscribers INTEGER)'''.format(self.database_table_subreddit_followers))
            dbc.commit()
        except Error as e:
            print(e)

    def get_tracked(self):
        dbc = sqlite3.connect(self.database_file)
        try:
            return dbc.execute('SELECT * FROM {}'.format(self.database_table_subreddit)).fetchall()
        except Error as e:
            print(e)
        dbc.close()

    def track(self, subreddit):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('INSERT INTO {} (name) VALUES (?)'.format(self.database_table_subreddit), (subreddit,))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def untrack(sefl, subreddit):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('DELETE FROM {} WHERE name=? LIMIT 1'.format(self.database_table_subreddit), (subreddit,))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def insert_subreddit(self, subreddit):
        dbc = sqlite3.connect(self.database_file)
        try:
            dbc.execute('INSERT INTO {} (name, subscribers) VALUES (?, ?)'.format(self.database_table_subreddit_followers), (subreddit.name, subreddit.subscribers))
        except Error as e:
            print(e)
        dbc.commit()
        dbc.close()

    def insert_subreddits(self, subreddits):
        dbc = sqlite3.connect(self.database_file)
        for subreddit in subreddits:
            try:
                dbc.execute('INSERT INTO {} (name, subscribers) VALUES (?, ?)'.format(self.database_table_subreddit_followers), (subreddit.name, subreddit.subscribers))
            except Error as e:
                print(e)            
        dbc.commit()
        dbc.close()
