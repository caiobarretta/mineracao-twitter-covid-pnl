import tweepy as tw

import yaml
from yaml.loader import SafeLoader

def get_credentials(file_name):
    with open(file_name) as f:
        data = yaml.load(f, Loader=SafeLoader)
    return data['consumer_key'],data['consumer_secret'],data['access_token'], data['access_token_secret']

def create_auth():
    consumer_key, consumer_secret, access_token, access_token_secret = get_credentials('src/credentials.yaml')
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def create_api():
    auth = create_auth()
    api = tw.API(auth)
    return api

def search_tweets(query, lang, count_of_tweets):
    api = create_api()
    tweets = tw.Cursor(api.search_tweets, q=query, lang=lang).items(count_of_tweets)
    return tweets

tweets = search_tweets('#SUS AND #COVID', 'pt', 1)
for tweet in tweets:
    print(tweet.text)