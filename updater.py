def update_token_metrics():
    db.TokenDB().insert(api.get_top_tokens())
    db.MarketCapitalizationDB().insert(api.get_mcap())

def update_twitter_data():
    try:
        file = open('api-creds-twitter.json', 'r')
        creds = model.OAuthCredentials.from_json(json.load(file))
        database = db.TwitterDB()
        names = database.get_tracked()
        for name in names:
            twitter = api.get_twitter(name, creds)
            if twitter is not None:
	            database.insert(twitter)
    except Exception:
        print("Could not load Twitter credentials, ensure api-creds-twitter.json exists and has a valid access_token")

def update_twitters():
    database = db.TwitterDB()
    for subscribable in api.get_top_twitters():
        database.track(subscribable)

def update_subreddit_data():
    database = db.RedditDB()
    names = database.get_tracked()
    for name in names:
        subreddit = api.get_subreddit(name)
        if subreddit is not None:
            database.insert(subreddit)

def update_subreddits():
    database = db.RedditDB()
    for subscribable in api.get_top_reddits():
        database.track(subscribable)

def main():
	print("Running HODLCORE updater...")
	update_token_metrics()
	update_twitters()
	update_twitter_data()
	update_subreddits()
	update_subreddit_data()
	print("Done!")


if __name__ == '__main__':
    sys.exit(main())