#!/usr/bin/env python
import sqlite
from sqlite3 import Error

__database_cmc_file = 'data/cmc.db'
__database_cmc_name = 'coinmarketcap'
__database_portfolio_name = 'portfolio'

def create_tables(c):
    try:
        # Create table
        c.execute('''CREATE TABLE %s
                    (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                     id TEXT,
                     name TEXT,
                     symbol TEXT,
                     rank INTEGER,
                     price_usd REAL,
                     price_btc REAL,
                     volume_usd REAL,
                     market_cap_usd REAL,
                     available_supply REAL)''' % __database_cmc_name)
        c.commit()
    except Error as e:
        print(e)

def insert_tokens(tokens):
	# create connection
    c = sqlite3.connect(__database_cmc_file)

    try:
        c.execute('SELECT * FROM %s LIMIT 1' % __database_cmc_name)
    except sqlite3.OperationalError:
        print('creating tables and exiting!')
        create_tables(c)
        c.commit()

    for token in tokens:
        try:
            c.execute('INSERT INTO %s(id, name, symbol, rank, price_usd, price_btc, volume_usd, market_cap_usd, available_supply) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)' % __database_cmc_name, (
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

    c.commit()

def fetch_token(id):
