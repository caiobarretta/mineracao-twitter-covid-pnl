import glob
import json
from os.path import exists

from TipoDeArquivos import TipoDeArquivos


def save_json(file_name, content, replace_existing_file = True):
        file_exists = False
        if not replace_existing_file:
            file_exists = exists(file_name)
        if not file_exists:
            with open(file_name, "w") as f:
                json.dump(content, f, indent=2)

def read_json(file_path):
    content = None
    with open(file_path) as f:
        content = json.load(f)
    return content

def get_file_list(path_tweets, extension_tweets):
    path_to_matching = f'{path_tweets}*{extension_tweets}'
    file_list = glob.glob(path_to_matching)
    return file_list

def retona_texto_json(path, extension, tipo_arquivo, data):
    file_list = get_file_list(path, extension)
    for file in file_list:
        content = read_json(file)
        print(f'processando arquivo: {file}')
        json = get_json_by_filetype(content, tipo_arquivo)
        data.append(json)

def get_json_by_filetype(content, tipo_arquivo):
    json = {}
    if tipo_arquivo == TipoDeArquivos.TWITTER:
        json = get_text_from_twitter_json_files(content)
    elif tipo_arquivo == TipoDeArquivos.YOUTUBE_COMMENTS:
        json = get_text_from_youtube_comments_json_files(content)
    else:
        raise Exception(f'Função para enum: {tipo_arquivo} não implementada.')
    json['src'] = str(tipo_arquivo.name)
    return json

def get_text_from_twitter_json_files(content):
    json = {}
    json['id'] = content['id']
    if 'full_text' in content:
        json['text'] = content['full_text']
    else:
        json['text'] = content['text']
    return json

def get_text_from_youtube_comments_json_files(content):
    json = {}
    json['id'] = content['id']
    json['text'] = content['snippet']['topLevelComment']['snippet']['textOriginal']
    return json

def save_data_partition(index, path, content, extension):
    file_name = f'{path}consolidado_part_{index}{extension}'
    save_json(file_name, content)

def save_consolidation_data_partition(path, data, extension, file_size):
    total_file_len = 0
    file_count = 0
    json_list = []
    for json in data:
        json_len =  get_string_dict_len(json)
        total_file_len = total_file_len + json_len
        json_list.append(json)
        if total_file_len >= file_size:
            save_data_partition(file_count, path, json_list, extension)
            file_count = file_count + 1
            json_list = []
            total_file_len = 0
    if file_count == 0:
        save_data_partition(file_count, path, json_list, extension)
        json_list = []
    if len(json_list):
        save_data_partition(file_count, path, json_list, extension)

def get_string_dict_len(json):
    id = json['id']
    text = json['text']
    src = json['src']
    full_string = '{' + f"'{id}','{text}','{src}'" + "},"
    return len(full_string.encode('utf-8'))

def main():
    
    path_raw = f'data/raw/'
    path_tweets = f'{path_raw}twitter/'
    path_youtube_comments = f'{path_raw}youtube/filtered_comment_threads/'
    extension = '.json'

    data = []
    retona_texto_json(path_tweets, extension, TipoDeArquivos.TWITTER, data)
    retona_texto_json(path_youtube_comments, extension, TipoDeArquivos.YOUTUBE_COMMENTS, data)

    file_size = 50 * 1048576 #~50MB
    save_consolidation_data_partition(path_raw, data, extension, file_size)

    path = f'{path_raw}consolidado_part_'
    file_list = get_file_list(path, extension)
    for file in file_list[0:1]:
        content = read_json(file)
        print(content)

if __name__ == '__main__':
    main()
