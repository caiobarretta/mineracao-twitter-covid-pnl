import glob
import json

def read_json(file_path):
    content = None
    with open(file_path) as f:
        content = json.load(f)
    return content


path_tweets = 'data/raw/twitter/'
extension_tweets = '.json'

path_tweets_to_matching = f'{path_tweets}*{extension_tweets}'

file_list = glob.glob(path_tweets_to_matching)

for file in file_list[0:1]:
    content = read_json(file)
    print(content['full_text'])

