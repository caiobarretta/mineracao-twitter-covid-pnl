import glob
import json
from os.path import exists
from time import sleep
from typing import Final

from TipoDeArquivos import TipoDeArquivos
from TrataEmoji import TrataEmoji
from Tradutor import Tradutor

class ConsolidaArquivos:

    PATH_RAW: Final[str] = f'data/raw/'
    PATH_TWEETS: Final[str] = f'{PATH_RAW}twitter/'
    PATH_YOUTUBE_COMMENTS: Final[str] = f'{PATH_RAW}youtube/filtered_comment_threads/'
    EXTENSION: Final[str] = '.json'

    def save_json(self, file_name, content, replace_existing_file = True):
            file_exists = False
            if not replace_existing_file:
                file_exists = exists(file_name)
            if not file_exists:
                with open(file_name, "w") as f:
                    json.dump(content, f, indent=2)

    def read_json(self, file_path):
        content = None
        with open(file_path) as f:
            content = json.load(f)
        return content

    def get_file_list(self, path, extension):
        path_to_matching = f'{path}*{extension}'
        file_list = glob.glob(path_to_matching)
        return file_list

    def retona_texto_json(self, path, extension, tipo_arquivo, data):
        file_list = self.get_file_list(path, extension)
        for file in file_list:
            content = self.read_json(file)
            print(f'processando arquivo: {file}')
            json = self.get_json_by_filetype(content, tipo_arquivo)
            data.append(json)

    def get_json_by_filetype(self, content, tipo_arquivo):
        json = {}
        if tipo_arquivo == TipoDeArquivos.TWITTER:
            json = self.get_text_from_twitter_json_files(content)
        elif tipo_arquivo == TipoDeArquivos.YOUTUBE_COMMENTS:
            json = self.get_text_from_youtube_comments_json_files(content)
        else:
            raise Exception(f'Função para enum: {tipo_arquivo} não implementada.')
        json['src'] = str(tipo_arquivo.name)
        return json

    def get_text_from_twitter_json_files(self, content):
        json = {}
        json['id'] = content['id']
        if 'full_text' in content:
            json['texto'] = content['full_text']
        else:
            json['texto'] = content['text']
        if 'text_tratado' in content:
            json['texto_tratado'] = content['text_tratado']
        return json

    def get_text_from_youtube_comments_json_files(self, content):
        json = {}
        json['id'] = content['id']
        json['texto'] = content['snippet']['topLevelComment']['snippet']['textOriginal']
        return json

    def save_data_partition(self, index, path, content, extension):
        file_name = f'{path}consolidado_part_{index}{extension}'
        self.save_json(file_name, content)

    def save_consolidation_data_partition(self, path, data, extension, file_size, tratar_emoji = False, traduzir_texto = False):
        tradutor = Tradutor()
        total_file_len = 0
        file_count = 0
        json_list = []
        for json in data:
            self.executa_tratamentos(json, tradutor, tratar_emoji, traduzir_texto)
            json_len =  self.get_string_dict_len(json)
            total_file_len = total_file_len + json_len
            json_list.append(json)
            if total_file_len >= file_size:
                self.save_data_partition(file_count, path, json_list, extension)
                file_count = file_count + 1
                json_list = []
                total_file_len = 0
        if file_count == 0:
            self.save_data_partition(file_count, path, json_list, extension)
            json_list = []
        if len(json_list):
            self.save_data_partition(file_count, path, json_list, extension)

    def get_string_dict_len(self, json):
        id = json['id']
        texto = json['texto']
        texto_tratado = json['texto']
        src = json['src']
        full_string = '{' + f"'{id}','{texto}','{texto_tratado}','{src}'" + "},"
        return len(full_string.encode('utf-8'))

    def executa_tratamentos(self, json, tradutor, tratar_emoji = False, traduzir_texto = False):
        if tratar_emoji:
            self.converter_emoji_em_texto(json)
        if traduzir_texto:
            self.traduzir_texto_portugues(json, tradutor)

    def converter_emoji_em_texto(self, json):
        print(f"Tratando emoji do texto id: {json['id']}")
        trataEmoji = TrataEmoji()
        json['texto_tratado'] = trataEmoji.converte_emoji_em_texto(json['texto'], ' ')

    def traduzir_texto_portugues(self, json, tradutor, sleep=10):
        sleep(sleep)
        print(f"Traduzindo texto id: {json['id']}")
        json['texto_tratado'] = tradutor.traducao_portugues(json['texto'])

def main():

    data = []
    consolidaArquivos = ConsolidaArquivos()
    path_raw = consolidaArquivos.PATH_RAW
    path_tweets = consolidaArquivos.PATH_TWEETS
    path_youtube_comments = consolidaArquivos.PATH_YOUTUBE_COMMENTS
    extension = consolidaArquivos.EXTENSION

    consolidaArquivos.retona_texto_json(path_tweets, extension, TipoDeArquivos.TWITTER, data)
    consolidaArquivos.retona_texto_json(path_youtube_comments, extension, TipoDeArquivos.YOUTUBE_COMMENTS, data)

    file_size = 50 * 1048576 #~50MB
    consolidaArquivos.save_consolidation_data_partition(path_raw, data, extension, file_size)

    path = f'{path_raw}consolidado_part_'
    file_list = consolidaArquivos.get_file_list(path, extension)
    for file in file_list:
        content = consolidaArquivos.read_json(file)
        print(content)

if __name__ == '__main__':
    main()
