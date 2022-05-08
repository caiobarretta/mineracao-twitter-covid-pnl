import tweepy as tw

import yaml
from yaml.loader import SafeLoader

class TweepyAPI:
    def __init__(self, file_name_credentials):
        self.file_name_credentials = file_name_credentials

    def get_credentials(self):
        with open(self.file_name_credentials) as f:
            data = yaml.load(f, Loader=SafeLoader)
        return data['consumer_key'],data['consumer_secret'],data['access_token'], data['access_token_secret']

    def create_auth(self):
        consumer_key, consumer_secret, access_token, access_token_secret = self.get_credentials()
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def create_api(self):
        auth = self.create_auth()
        api = tw.API(auth)
        return api

    def search_tweets(self, query, lang, count_of_tweets = 0):
        api = self.create_api()
        tweets = tw.Cursor(api.search_tweets, q=query, lang=lang, tweet_mode = "extended").items()
        if(count_of_tweets > 0):
            tweets = tweets.items(count_of_tweets)
        return tweets
    
    def get_api_name(self):
        return 'Twitter'