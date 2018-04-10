#!/usr/bin/env python
import math
from operator import attrgetter

__emojis = {
    'poop':             u'\U0001f4a9',
    'crashing':         u'\U0001f4c9',
    'mooning':          u'\U0001f4c8',
    'rocket':           u'\U0001f680',
    'charts':           u'\U0001f4ca',
    'pause':            u'\U000023f8',
    'sleeping':         u'\U0001f634',
    'dollar':           u'\U0001f4b5',
    'triangle_up':      u'\U0001f53a',
    'triangle_dn':      u'\U0001f53b',
    'apple_green':      u'\U0001f34f',
    'apple_red':        u'\U0001f34e',
    'pear':             u'\U0001f350',
    'vs':               u'\U0001f19a',
    'squirt':           u'\U0001f4a6',
    'umbrella':         u'\U00002614',
    'fire':             u'\U0001f525',
    'arrow_up':         u'\U00002197',
    'arrow_down':       u'\U00002198',
    'collision':        u'\U0001f4a5',
    'rainbow':          u'\U0001f308',
    'carlos':           u'\U0001f919',
    'skull':            u'\u2620\ufe0f',
    'broken_heart':     u'\U0001f494',
    'green_heart':      u'\U0001f49a',
    'orange_diamond':   u'\U0001f538',
}


def emoji(key):
    try:
        return __emojis[key].encode('utf-8')
    except:
        return ''


def large_number(n, short=False):
    """ Return human readable large numbers. """
    if short:
        millnames = ['','k','m','bn','tn']
    else:
        millnames = ['','k','Million','Billion','trillion']
    try:
        n = float(n)
        millidx = max(0, min(len(millnames)-1,
        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
        return '{:.0f} {}'.format(n / 10**(3 * millidx), millnames[millidx])
    except TypeError:
        return '?'


def sh_color(n):
	default_color_prefix = '\033[39m'
	color_prefix = default_color_prefix
	if n > 0:
		color_prefix = '\033[38;5;2m'
	elif n < 0:
		color_prefix = '\033[38;5;1m'
	return '{}{}{}'.format(color_prefix, n, default_color_prefix)


def percent(num, emo=True):
    if not emo:        
        return '{}{:.2f}%'.format('+' if num > 0 else '', num)
    else:
        if num > 0:
            prefix = '{} +'.format(emoji('green_heart'))
        elif num == 0:
            prefix = '{}  '.format(emoji('orange_diamond'))
        else:
            prefix = '{} '.format(emoji('broken_heart'))
        return '{}{:.2f}%'.format(prefix, num)


def mcap_summary(mcap):
    s = '*Global data {}:*\n'.format(emoji('charts'))
    s += '\t*Total Market Cap (USD):* ${}\n'.format(large_number(mcap.mcap_usd))
    s += '\t*Total 24h Volume USD):* ${}\n'.format(large_number(mcap.volume_usd_24h))
    s += '\t*BTC Dominance:* {}'.format(percent(mcap.bitcoin_percentage_of_market_cap, emo=False))
    return s


def token_summary(token, btc_summary = None):
    s = '*{} ({}) {}*:\n'.format(token.name, token.symbol.upper(), emoji('charts'))
    s += '\t*Rank:* #{}\n'.format(token.rank)
    s += '\t*Price (USD):* ${}\n'.format(token.price)
    if btc_summary is not None:
        s += '\t*Price (BTC):* {}\n'.format(token.price_btc)
    s += '\t*24h Volume:* {}\n'.format(large_number(token.volume_24h))
    s += '\t*Market Cap:* {}\n'.format(large_number(token.mcap))
    s += '\t*Avail. Supply:* {}\n'.format(large_number(token.available_supply))
    s += '\t*Total Supply:* {}\n'.format(large_number(token.total_supply))
    s += '\t*Max Supply:* {}\n'.format(large_number(token.max_supply))
    s += '\t*Change (USD):*\n'
    s += '```\t\t 1h: {}\n'.format(percent(token.percent_change_1h, emo=True))
    s += '\t\t24h: {}\n'.format(percent(token.percent_change_24h, emo=True))
    s += '\t\t 7d: {}```'.format(percent(token.percent_change_7d, emo=True))
    if btc_summary is not None:
        s += '\n\t*Change (BTC)*:\n'
        s += '```\t\t24h: {}\n'.format(percent(btc_summary.pct_today, emo=True))
        s += '\t\t 7d: {}\n'.format(percent(btc_summary.pct_week, emo=True))
        s += '\t\t30d: {}```'.format(percent(btc_summary.pct_month, emo=True))

    return s


def token_compared_summary(token, other_token):
    s = '*{} {} {}*:\n'.format(token.name, emoji('vs'), other_token.name)
    s += '\t*Rank:* #{} vs #{}\n'.format(token.rank, other_token.rank)
    s += '\t*Price (USD):* ${} vs ${}\n'.format(token.price, other_token.price)
    s += '\t*Price (BTC):* {} vs {}\n'.format(token.price_btc, other_token.price_btc)
    s += '\t*24h Volume:* {} vs {}\n'.format(large_number(token.volume_24h), large_number(other_token.volume_24h))
    s += '\t*Market Cap:* {} vs {}\n'.format(large_number(token.mcap), large_number(other_token.mcap))
    s += '\t*Avail. Supply:* {} vs {}\n'.format(large_number(token.available_supply), large_number(other_token.available_supply))
    s += '\t*Total Supply:* {} vs {}\n'.format(large_number(token.total_supply), large_number(other_token.total_supply))
    s += '\t*Max Supply:* {} vs {}\n'.format(large_number(token.max_supply), large_number(other_token.max_supply))
    s += '\t*Change (USD):*\n'
    s += '```\t\t 1h:  {} vs {}\n'.format(percent(token.percent_change_1h, emo=True), percent(other_token.percent_change_1h, emo=True))
    s += '\t\t24h: {} vs {}\n'.format(percent(token.percent_change_24h, emo=True), percent(other_token.percent_change_24h, emo=True))
    s += '\t\t 7d:  {} vs {}```'.format(percent(token.percent_change_7d, emo=True), percent(other_token.percent_change_7d, emo=True))
    mcap = other_token.mcap / token.mcap
    mcap_price = mcap * other_token.price
    vol_factor = other_token.volume_24h / token.volume_24h
    s += '\t*{} has {:.2f}x  the 24h volume of {}.*\n\n'.format(other_token.name, vol_factor, token.name)
    s += '\t*If {} had the cap of {}, the USD price would be: ${} ({:.1f}x)*'.format(token.name, other_token.name, mcap_price, mcap)
    return s


def airdrop_summary(airdrop):
    if airdrop.today:
        return "\t- *{}* (*today*)\n".format(airdrop.title)
    elif airdrop.ongoing:
        return "\t- *{}* (*ongoing*)\n".format(airdrop.title)
    elif airdrop.finished:
        return "\t- *{}* (*finished*)\n".format(airdrop.title)
    else:
        return "\t- *{}* (*in {} days*)\n".format(airdrop.title, airdrop.when.days)


def airdrops_summary(airdrops, limit = 20):
    text = "*Upcoming Airdrops{}:*\n".format(emoji('squirt'))
    for airdrop in sorted(airdrops, key=attrgetter('when.days'), reverse=False)[:limit]:
        text += airdrop_summary(airdrop)
    return text


def token_ranks_summary(token, ranks):
    triangle = stringformat.emoji('triangle_up')
    return '\t-{}*{}* ({}/{}): *{}* ({}, #{})\n'.format(triangle, -ranks.diff_today, -ranks.diff_week, -ranks.diff_month, token.name, token.symbol, ranks.now)

def tokens_ranks_summary(token_ranks):
    text = '*CoinMarketCap rank climbers (w/m):*\n'
    for (token, ranks) in token_ranks:
        text += token_ranks_summary(token, ranks)
    text += '\nShowing All Time High ranks only {}'.format(stringformat.emoji('fire'))
    return text
