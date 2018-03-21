#!/usr/bin/env python
import requests
import json
import model
from bs4 import BeautifulSoup
import tweepy
import datetime

import stringformat

__endpoint_tokens_all = 'https://api.coinmarketcap.com/v1/ticker/?limit=10000'
__endpoint_tokens_limit = 'https://api.coinmarketcap.com/v1/ticker/?limit={}'
__endpoint_token_scrape = 'https://coinmarketcap.com/currencies/{}'
__endpoint_token_scrape_social = 'https://coinmarketcap.com/currencies/{}/#social'
__endpoint_token = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'
__endpoint_mcap = 'https://api.coinmarketcap.com/v1/global/'
__endpoint_subreddits = 'https://www.reddit.com/r/{}/about.json'
__endpoint_twitter = 'https://www.reddit.com/r/{}/about.json'
__endpoint_ico = 'https://icodrops.com/{}'
__endpoint_airdrop = 'https://coindar.org/en/tags/airdrop'

__headers_useragent = { 'User-agent': 'hodlcore beta' }
__headers_mozilla = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
}


def get_portfolio(portfolio_config, currency):
    portfolio = model.Portfolio()
    for item in portfolio_config:
        token = get_token(item[0], item[1], currency)
        if token is not None:
            portfolio.add_token(token)
    return portfolio


def get_mcap():
    mcap_json = requests.get(__endpoint_mcap).json()
    return model.MarketCapitalization.from_json(mcap_json)


def get_token(name, balance = 0 , currency = 'usd'):
    try:
        r_token = requests.get(__endpoint_token.format(name, currency)).json()[0]
        return model.Token.from_json(r_token, balance, currency)
    except:
        return None


def get_top_tokens(limit = 100):
    r_tokens = requests.get(__endpoint_tokens_limit.format(limit)).json()
    tokens = []
    for r_token in r_tokens:
        try:
            tokens.append(model.Token.from_json(r_token))
        except:
            pass
    return tokens


def search_tokens(search, limit = 100):
    r_tokens = requests.get(__endpoint_tokens_all).json()
    tokens = []
    for r_token in r_tokens:
        try:
            token = model.Token.from_json(r_token)
            if token.matches(search):
                tokens.append(token)
            if len(tokens) >= limit:
                break
        except:
            pass
    return tokens


def search_token(search):
    try:
        return search_tokens(search, limit=1)[0]
    except:
        return None


def get_top_subreddits(limit = 300):
    top_tokens = get_top_tokens(limit=limit)
    subscribables = []
    for token in top_tokens:
        r = requests.get(__endpoint_token_scrape_social.format(token.id))
        lines = r.text.split('\n')
        for line in lines:
            if 'www.reddit.com' in line:
                try:
                    reddit = line.split('"')[1].split('/')[4].split('.')[0]
                    subscribables.append(reddit)
                except IndexError:
                    pass
    return subscribables


def get_top_twitters(limit = 300):
    top_tokens = get_top_tokens(limit=limit)
    subscribables = []
    for token in top_tokens:
        token_scrape = requests.get(__endpoint_token_scrape.format(token.id))
        soup = BeautifulSoup(token_scrape.text, 'lxml')
        try:
            twitter = soup.find('a', 'twitter-timeline').attrs['data-screen-name']
            subscribables.append(twitter)
        except:
            pass
    return subscribables


def get_subreddit(subreddit):
    try:
        r_subreddit = requests.get(__endpoint_subreddits.format(subreddit), headers = __headers_useragent).json()['data']
        return model.Subscribable(subreddit, r_subreddit['subscribers'], r_subreddit['url'])
    except KeyError:
        return None


def get_twitter(twitter, credentials):
    auth = tweepy.auth.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)
    tweepy_api = tweepy.API(auth)
    try:
        user = tweepy_api.get_user(twitter)
        return model.Subscribable(twitter, user.followers_count, 'https://twitter.com/{}'.format(twitter))
    except tweepy.error.TweepError:
        return None


def get_ico_text(token):
    try:
        ico_response = requests.get(__endpoint_ico.format(token.id.lower()), headers=__headers_mozilla)
        soup = BeautifulSoup(ico_response.text, 'lxml')
        rel_sections = soup.find_all('div', 'white-desk ico-desk')
        fields = [
            'ticker:',
            'ico token price:',
            'total tokens:',
            'accepts:',
        ]
        entries = []
        for s in rel_sections:
            if not s.find_all('i', 'fa fa-calendar'):
                continue

            # ICO details
            ico_info = s.find('div', 'col-12 col-md-6')
            lines = s.find_all('li')
            for line in lines:
                for field in fields:
                    if field in line.text.lower():
                        header, value = line.text.encode('utf-8').split(':')
                        entries.append('\t*{}*: {}\n'.format(header, value))

            # Price lists
            prices = soup.find('div', 'token-price-list').find_all('li')
            price_list = []
            for price in prices:
                price_list.append('\t\t{}\n'.format(price.text.encode('utf-8')))

            # ROIs
            rois = soup.find('div', 'col-12 col-md-6 ico-roi').find_all('li')
            roi_list = []
            for roi in rois:
                amount = roi.find('div', 'roi-amount').text.encode('utf-8')
                currency = roi.find('div', 'roi-currency').text.encode('utf-8')
                roi_list.append('\t*Returns {}*: {}'.format(currency, amount))

        if entries:
            text = '*ICO Information for {}{}:*\n'.format(token.name_str, stringformat.emoji('charts'))
            text += '{}\n'.format(entries)
            if price_list:
                text += '\t*Token Price List:*\n{}\n'.format(price_list)
            if roi_list:
                text += '\n{}'.format(roi_list)

            return text
        else:
            return None
    except Exception as e:
        print(token)
        print(e)
        return None


def get_airdrops():
    airdrop_response = requests.get(__endpoint_airdrop)
    events = BeautifulSoup(airdrop_response.text, 'lxml').find_all('div', 'addeventatc')
    now = datetime.datetime.now()
    airdrops = []
    for e in events:
        try:
            start = datetime.datetime.strptime(e.find('span', 'start').text[:10], '%m/%d/%Y')
            end = datetime.datetime.strptime(e.find('span', 'end').text[:10], '%m/%d/%Y')
            title = e.find('span', 'title').text
            airdrop = model.Event(title, start, end)
            airdrops.append(airdrop)
        except Exception as e:
            print(e)
            pass
    return airdrops
