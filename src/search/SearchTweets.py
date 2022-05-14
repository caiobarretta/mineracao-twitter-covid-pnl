import json
import time
from tweepy.errors import TooManyRequests
from SearchBase import SearchBase
from SearchKeys import SearchKeys

from api.TweepyAPI import TweepyAPI

class SearchTweets(SearchBase):
    def __init__(self, replace_existing_tweets = True, yt_time_sleep_load_search = 20):
        self.replace_existing_tweets = replace_existing_tweets
        super().__init__(yt_time_sleep_load_search)

    def save_tweets(self, tweets):
        try:
            for tweet in tweets:
                print(f'salvando tweet: {tweet.id} para arquivo.')
                file_name = f'data/raw/twitter/{tweet.id}.json'
                content = tweet._json
                self.save_json(file_name, content, self.replace_existing_tweets)
                time.sleep(1)
        except TooManyRequests:
                print(f'Ocorreu um erro: {TooManyRequests}')

    def get_and_save_tweets(self, api, query, lang):
        print(f'carregando os tweets da pesquisa: {query}|{lang}')
        tweets = api.search_tweets(query, lang)
        print(f'tweets da pesquisa: {query}|{lang} carregados com sucesso.')
        self.save_tweets(tweets)

    def get_new_instance_api(self, file_credentials):
        return TweepyAPI(file_credentials)

def main():
    search = SearchTweets(False)
    file_credentials = 'src/credentials.yaml'

    func_get_new_instance_api = search.get_new_instance_api
    func_get_query_to_search = SearchKeys('pt').get_twitter_query_covid_lang
    func_get_and_save_data = search.get_and_save_tweets

    pesquisa = search.load_search_query_list_dict(func_get_query_to_search)

    search.load_search(file_credentials, pesquisa, func_get_new_instance_api, func_get_and_save_data)

if __name__ == '__main__':
    main()
