import glob
import json
import csv


def write_csv_consolidado(path_csv, headers, data):
    with open(path_csv, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(data)

def read_json(file_path):
    content = None
    with open(file_path) as f:
        content = json.load(f)
    return content

def retona_texto_tweets(path_tweets, extension_tweets):
    path_to_matching = f'{path_tweets}*{extension_tweets}'
    file_list = glob.glob(path_to_matching)
    list_text = []
    headers = ['id', 'text']
    for file in file_list:
        content = read_json(file)
        id_tweet = content['id']
        text = ''
        list_fields = []
        if 'full_text' in content:
            text = content['full_text']
        else:
            text = content['text']
        list_fields.append(id_tweet)
        list_fields.append(text)
        list_text.append(list_fields)
    return headers, list_text

def main():
    path_tweets = 'data/raw/twitter/'
    extension_tweets = '.json'

    headers, data = retona_texto_tweets(path_tweets, extension_tweets)
    path_csv = f'{path_tweets}consolidado.csv'

    write_csv_consolidado(path_csv, headers, data)

if __name__ == '__main__':
    main()
