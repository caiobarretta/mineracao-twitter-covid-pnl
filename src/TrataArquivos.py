import time
from TrataEmoji import TrataEmoji
from ConsolidaArquivos import ConsolidaArquivos
from TipoDeArquivos import TipoDeArquivos
from Tradutor import Tradutor
from RemocaoDeUrl import RemocaoDeUrl
from CorrigiOrtografiaForaDoPadrao import CorrigiOrtografiaForaDoPadrao
from DividePalavrasUnidas import DividePalavrasUnidas
from RemoveElementosDeMarcacao import RemoveElementosDeMarcacao

class TrataArquivos:
    def __init__(self, consolidaArquivos, tratamento, time_sleep_load_tratamento = 5):
        self.time_sleep_load_tratamento = time_sleep_load_tratamento
        self.consolidaArquivos = consolidaArquivos
        self.tratamento = tratamento

    def tratar_arquivos(self, path, extension, tipo_arquivo, refazer_tratamento=False, propriedade_json = 'texto'):
        print('carregando lista de arquivos')
        file_list = self.consolidaArquivos.get_file_list(path, extension)
        self.tratar_arquivo(file_list, tipo_arquivo, refazer_tratamento, propriedade_json)

    def tratar_arquivo(self, file_list, tipo_arquivo, refazer_tratamento, propriedade_json):
        for file in file_list:
            print(f'Lendo arquivo: {file}')
            content = self.consolidaArquivos.read_json(file)
            if tipo_arquivo == TipoDeArquivos.TWITTER:
                self.tratar_arquivos_twitter(file, content, refazer_tratamento, propriedade_json)
            elif tipo_arquivo == TipoDeArquivos.YOUTUBE_COMMENTS:
                self.tratar_arquivos_youtube(file, content, refazer_tratamento, propriedade_json)
            else:
                raise Exception(f'Função para enum: {tipo_arquivo} não implementada.')

    def tratar_arquivos_twitter(self, file, content, refazer_tratamento, propriedade_json):
        node_dest = 'text_tratado'
        if node_dest in content and not refazer_tratamento:
            return
        print(f'processando arquivo: {file}')
        get_text_from_files = self.consolidaArquivos.get_text_from_twitter_json_files
        get_text_from_json = self.get_text_from_json_twitter
        set_text_from_json = self.set_text_from_json_twitter
        self.processa_tratamento_arquivos(file, content, get_text_from_files, get_text_from_json, set_text_from_json, propriedade_json)
    
    def tratar_arquivos_youtube(self, file, content, refazer_tratamento, propriedade_json):
        node_dest = 'text_tratado'
        if node_dest in content and not refazer_tratamento:
            return
        print(f'processando arquivo: {file}')
        get_text_from_files = self.consolidaArquivos.get_text_from_youtube_comments_json_files
        get_text_from_json = self.get_text_from_json_youtube
        set_text_from_json = self.set_text_from_json_youtube
        self.processa_tratamento_arquivos(file, content, get_text_from_files, get_text_from_json, set_text_from_json, propriedade_json)

    def get_text_from_json_twitter(self, json, propriedade_json):
        if propriedade_json in json:
            return json[propriedade_json]
        return json['texto']

    def get_text_from_json_youtube(self, json, propriedade_json):
        if propriedade_json in json:
            return json[propriedade_json]
        return json['texto']

    def set_text_from_json_twitter(self, json, texto):
        json['text_tratado'] = texto

    def set_text_from_json_youtube(self, json, texto):
        json['text_tratado'] = texto

    def processa_tratamento_arquivos(self, file, content, get_text_from_files, get_text_from_json, set_text_from_json, propriedade_json):
        json_content = get_text_from_files(content)
        texto = get_text_from_json(json_content, propriedade_json)

        texto_sem_emoji = self.resolve_tratamento_texto_ioc(texto)
        
        set_text_from_json(content, texto_sem_emoji)
        self.consolidaArquivos.save_json(file, content)
        time.sleep(self.time_sleep_load_tratamento)

    def resolve_tratamento_texto_ioc(self, texto):
        if type(self.tratamento ) is list:
            for classe_tratamento in self.tratamento:
                if type(classe_tratamento) is dict:
                    if classe_tratamento['Executar']:
                        return classe_tratamento['Classe'].tratar_texto(texto)
                    else:
                        return texto
                else:
                    return classe_tratamento.tratar_texto(texto)
        else:
            return self.tratamento.tratar_texto(texto)

def test_tratar_arquivo():
    trataEmoji = TrataEmoji(Tradutor())
    consolidaArquivos = ConsolidaArquivos()
    trataArquivos = TrataArquivos(consolidaArquivos, trataEmoji, 0)
    path_tweets = consolidaArquivos.PATH_TWEETS
    extension = consolidaArquivos.EXTENSION
    file_list = consolidaArquivos.get_file_list(path_tweets, extension)[0:50]
    trataArquivos.tratar_arquivo(file_list, TipoDeArquivos.TWITTER, True)

def test_tratar_arquivo_lst_classe_tratamento():
    remocaoDeUrl = RemocaoDeUrl()
    trataEmoji = TrataEmoji(Tradutor())
    dividePalavrasUnidas = DividePalavrasUnidas()
    removeElementosDeMarcacao = RemoveElementosDeMarcacao()
    corrigiOrtografiaForaDoPadrao = CorrigiOrtografiaForaDoPadrao()
    classe_tratar_arquivo_lst = [trataEmoji, corrigiOrtografiaForaDoPadrao, dividePalavrasUnidas,
        remocaoDeUrl, removeElementosDeMarcacao]
    consolidaArquivos = ConsolidaArquivos()
    trataArquivos = TrataArquivos(consolidaArquivos, classe_tratar_arquivo_lst, 0)
    path_tweets = consolidaArquivos.PATH_TWEETS
    extension = consolidaArquivos.EXTENSION
    file_list = consolidaArquivos.get_file_list(path_tweets, extension)[0:50]
    trataArquivos.tratar_arquivo(file_list, TipoDeArquivos.TWITTER, True)
    
def test_lista_de_classes():
    texto = "Una gran informaci\u00f3n y es una gran preocupaci\u00f3n hasta donde llega la ignorancia de las personas  al desechar todas sus basuras a los r\u00edos y mares no tomando en cuenta que estamos cavando nuestra propia tumba  al esparcir todos estos virus en  lo que nos da la vida, el agua, de verdad es muy preocupante ver los r\u00edos infestados de cubre bocas  y basura desechos de toda esta pandemia.  Saludos y muchas felicidades por su valiosa informaci\u00f3n."
    remocaoDeUrl = RemocaoDeUrl()
    trataEmoji = TrataEmoji(Tradutor())
    dividePalavrasUnidas = DividePalavrasUnidas()
    removeElementosDeMarcacao = RemoveElementosDeMarcacao()
    corrigiOrtografiaForaDoPadrao = CorrigiOrtografiaForaDoPadrao()
    classe_tratar_arquivo_lst = [trataEmoji, corrigiOrtografiaForaDoPadrao, dividePalavrasUnidas,
        remocaoDeUrl, removeElementosDeMarcacao]
    for classe_tratar_arquivo in classe_tratar_arquivo_lst:
        texto_tratado = classe_tratar_arquivo.tratar_texto(texto)
        print('texto_tratado:', texto_tratado)

def tests():
    test_tratar_arquivo()
    test_tratar_arquivo_lst_classe_tratamento()
    test_lista_de_classes()

def carrega_classe_tratar_arquivo_lst(remocao_de_url = True, trata_emoji = True, divide_palavras_unidas = True, corrigi_ortografia_fora_do_padrao = True, remove_elementos_de_marcacao = True):
    classe_tratar_arquivo_lst = []
    if remocao_de_url:
        classe_tratar_arquivo_lst.append(RemocaoDeUrl())
    if trata_emoji:
        classe_tratar_arquivo_lst.append(TrataEmoji(Tradutor()))
    if divide_palavras_unidas:
        classe_tratar_arquivo_lst.append(DividePalavrasUnidas())
    if corrigi_ortografia_fora_do_padrao:
        classe_tratar_arquivo_lst.append(CorrigiOrtografiaForaDoPadrao())
    if remove_elementos_de_marcacao:
        classe_tratar_arquivo_lst.append(RemoveElementosDeMarcacao())
    return classe_tratar_arquivo_lst

def main():
    classe_tratar_arquivo_lst = carrega_classe_tratar_arquivo_lst(True, False, False, False, False)
    consolidaArquivos = ConsolidaArquivos()
    path_tweets = consolidaArquivos.PATH_TWEETS
    path_youtube_comments = consolidaArquivos.PATH_YOUTUBE_COMMENTS
    extension = consolidaArquivos.EXTENSION
    trataArquivos = TrataArquivos(consolidaArquivos, classe_tratar_arquivo_lst, 0)
    trataArquivos.tratar_arquivos(path_tweets, extension, TipoDeArquivos.TWITTER, True, 'texto_tratado')
    trataArquivos.tratar_arquivos(path_youtube_comments, extension, TipoDeArquivos.YOUTUBE_COMMENTS, True, 'texto_tratado')

if __name__ == '__main__':
    main()