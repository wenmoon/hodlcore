#!/usr/bin/env python
import math

emojis = {
    'poop':     u'\U0001f4a9',
    'crashing': u'\U0001f4c9',
    'mooning':  u'\U0001f4c8',
    'rocket':   u'\U0001f680',
    'charts':   u'\U0001f4ca',
    'pause':    u'\U000023f8',
    'sleeping':    u'\U0001f634',
    'dollar':      u'\U0001f4b5',
    'triangle_up': u'\U0001f53a',
    'triangle_dn': u'\U0001f53b',
    'apple_green': u'\U0001f34f', # green apple
    'apple_red':   u'\U0001f34e', # red apple
    'pear':        u'\U0001f350', # pear
    'vs':          u'\U0001f19a',
    'squirt':      u'\U0001f4a6',
    'umbrella':    u'\U00002614',
    'fire':        u'\U0001f525',
    'arrow_up':    u'\U00002197',
    'arrow_down':  u'\U00002198',
    'collision':   u'\U0001f4a5',
    'rainbow':     u'\U0001f308',
    'carlos':      u'\U0001f919',
    'skull':       u'\u2620\ufe0f', #U+2620, U+FE0F
}

def large_number(n, short=False):
    """ Return human readable large numbers. """
    millnames = ['','k','m','bn','tn']
    try:
        n = float(n)
        millidx = max(0, min(len(millnames)-1,
        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
        return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
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


def percent(num, emoji=True):
    ret = '{:.0f}%'.format(num)
    if emoji:
        if num > 0:
            prefix = emojis['apple_green']
        elif num == 0:
            prefix = emojis['apple_green']
        else:
            prefix = emojis['pear']
        ret = '{} {}'.format(prefix, ret)
    return ret
