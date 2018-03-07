#!/usr/bin/env python
import sqlite
import time

__database_file = 'data/hodl.db'
__database_table_cmc_tokens = 'coinmarketcap_tokens'
__database_table_cmc_mcap = 'coinmarketcap_mcap'
__database_table_subreddit = 'subreddit'
__database_table_twitter = 'twitter'


class MarketCapitalizationDB(object):
    def __init__(self):
        dbc = sqlite3.connect(__database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1').format(__database_table_cmc)
        except sqlite3.OperationalError:
            create_tables(dbc)


    def create_tables(dbc):
        try:
            # Create table
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         mcap TEXT,
                         volume REAL)'''.format(__database_cmc_name))
            dbc.commit()
        except Error as e:
            print(e)

    def insert_mcap(mcap):
        for token in tokens:
            try:
                dbc.execute('''INSERT INTO {}
                    (mcap, volume) 
                     VALUES (?, ?)'''.format(__database_table_cmc_tokens), (
                        mcap.mcap_usd
                        mcap.volume_usd_24h))
            except KeyError:
                print('Error importing mcap: %s' % mcap)
        dbc.commit()



class CoinmarketcapDB(object):
    def __init__(self):
        # create connection
        dbc = sqlite3.connect(__database_file)

        try:
            dbc.execute('SELECT * FROM {} LIMIT 1').format(__database_table_cmc_tokens)
        except sqlite3.OperationalError:
            create_tables(dbc)


    def create_tables(dbc):
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
                         available_supply REAL)'''.format(__database_table_cmc_tokens))
            dbc.commit()
        except Error as e:
            print(e)

    def insert_tokens(tokens):
        dbc = sqlite3.connect(__database_file)
        for token in tokens:
            try:
                dbc.execute('''INSERT INTO {}
                    (id, name, symbol, rank, price_usd, price_btc,
                     volume_usd, market_cap_usd, available_supply) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''.format(__database_table_cmc_tokens), (
                        token.id,
                        token.name,
                        token.symbol,
                        token.rank,
                        token.price_usd,
                        token.price_btc,
                        token.volume_usd,
                        token.market_cap_usd,
                        token.available_supply,))
            except KeyError:
                print('Error importing token: %s' % token)
        dbc.commit()


class RedditDB(object):
    # TODO dump prod db here
    default_subreddits = [
        'bitcoin',
        'ethereum',
        'litecoin',
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

    def __init__(self):
        dbc = sqlite3.connect(__database_file)
        try:
            dbc.execute('SELECT * FROM {} LIMIT 1'.format(__database_table_subreddit))
        except sqlite3.OperationalError:
            create_tables(c)

    def create_tables(dbc):
        try:
            # Create table
            dbc.execute('''CREATE TABLE {}
                        (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        name TEXT,
                        subscribers INTEGER)'''.format(__database_table_subreddit))
            dbc.commit()
        except Error as e:
            print(e)

    def insert_subreddit(subreddit):
        dbc = sqlite3.connect(__database_file)
        dbc.execute('INSERT INTO {}(subreddit, followers) VALUES (?, ?)'.format(__database_table_subreddit_followers), (subreddit.name, subreddit.subscribers))
        dbc.commit()

    def insert_subreddits(subreddits):
        dbc = sqlite3.connect(__database_file)
        for subreddit in subreddits:
            dbc.execute('INSERT INTO {}(subreddit, followers) VALUES (?, ?)'.format(__database_table_subreddit_followers), (subreddit.name, subreddit.subscribers))
        dbc.commit()


# class TwitterDB(object):
#     def __init__(self):
#         dbc = sqlite3.connect(__database_file)
#         try:
#             dbc.execute('SELECT * FROM {} LIMIT 1'.format(__database_table_twitter))
#         except sqlite3.OperationalError:
#             create_tables(c)

#     def create_tables(dbc):
#         try:
#             dbc.execute('''CREATE TABLE {}
#                     (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, user TEXT, followers INTEGER)'''.format(__database_table_twitter))
#             dbc.commit()
#         except Error as e:
#             print(e)
