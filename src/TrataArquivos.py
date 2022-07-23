import time
from TrataEmoji import TrataEmoji
from ConsolidaArquivos import ConsolidaArquivos
from TipoDeArquivos import TipoDeArquivos
from Tradutor import Tradutor

class TrataArquivos:
    def __init__(self, consolidaArquivos, tratamento, time_sleep_load_tratamento = 5):
        self.time_sleep_load_tratamento = time_sleep_load_tratamento
        self.consolidaArquivos = consolidaArquivos
        self.tratamento = tratamento

    def tratar_arquivos(self, path, extension, tipo_arquivo, refazer_tratamento=False):
        print('carregando lista de arquivos')
        file_list = self.consolidaArquivos.get_file_list(path, extension)
        self.tratar_arquivo(file_list, tipo_arquivo, refazer_tratamento)

    def tratar_arquivo(self, file_list, tipo_arquivo, refazer_tratamento):
        for file in file_list:
            print(f'Lendo arquivo: {file}')
            content = self.consolidaArquivos.read_json(file)
            if tipo_arquivo == TipoDeArquivos.TWITTER:
                self.tratar_arquivos_twitter(file, content, refazer_tratamento)
            elif tipo_arquivo == TipoDeArquivos.YOUTUBE_COMMENTS:
                self.tratar_arquivos_youtube(file, content, refazer_tratamento)
            else:
                raise Exception(f'Função para enum: {tipo_arquivo} não implementada.')

    def tratar_arquivos_twitter(self, file, content, refazer_tratamento):
        node_dest = 'text_tratado'
        if node_dest in content and not refazer_tratamento:
            return
        print(f'processando arquivo: {file}')
        get_text_from_files = self.consolidaArquivos.get_text_from_twitter_json_files
        get_text_from_json = self.get_text_from_json_twitter
        set_text_from_json = self.set_text_from_json_twitter
        self.processa_tratamento_arquivos(file, content, get_text_from_files, get_text_from_json, set_text_from_json)

    def get_text_from_json_twitter(self, json):
        return json['texto']

    def get_text_from_json_youtube(self, json):
        return json['texto']

    def set_text_from_json_twitter(self, json, texto):
        json['text_tratado'] = texto

    def set_text_from_json_youtube(self, json, texto):
        json['text_tratado'] = texto

    def processa_tratamento_arquivos(self, file, content, get_text_from_files, get_text_from_json, set_text_from_json):
        json_content = get_text_from_files(content)
        texto = get_text_from_json(json_content)
        texto_sem_emoji = self.tratamento.tratar_texto(texto)
        set_text_from_json(content, texto_sem_emoji)
        self.consolidaArquivos.save_json(file, content)
        time.sleep(self.time_sleep_load_tratamento)

    def tratar_arquivos_youtube(self, file, content, refazer_tratamento):
        node_dest = 'textTratado'
        if node_dest in content and not refazer_tratamento:
            return
        print(f'processando arquivo: {file}')
        get_text_from_files = self.consolidaArquivos.get_text_from_youtube_comments_json_files
        get_text_from_json = self.get_text_from_json_youtube
        set_text_from_json = self.set_text_from_json_youtube
        self.processa_tratamento_arquivos(file, content, get_text_from_files, get_text_from_json, set_text_from_json)

def main():
    tradutor = Tradutor()
    trataEmoji = TrataEmoji(tradutor)
    consolidaArquivos = ConsolidaArquivos()

    path_tweets = consolidaArquivos.PATH_TWEETS
    path_youtube_comments = consolidaArquivos.PATH_YOUTUBE_COMMENTS
    extension = consolidaArquivos.EXTENSION

    trataArquivos = TrataArquivos(consolidaArquivos, trataEmoji, 5)
    trataArquivos.tratar_arquivos(path_tweets, extension, TipoDeArquivos.TWITTER)

if __name__ == '__main__':
    main()