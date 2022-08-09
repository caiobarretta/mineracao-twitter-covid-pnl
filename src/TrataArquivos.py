import time
from typing import Tuple
from TrataEmoji import TrataEmoji
from ConsolidaArquivos import ConsolidaArquivos
from TipoDeArquivos import TipoDeArquivos
from VerificaIdioma import VerificaIdioma
from Tradutor import Tradutor
from RemocaoDeUrl import RemocaoDeUrl
from CorrigiOrtografiaForaDoPadrao import CorrigiOrtografiaForaDoPadrao
from DividePalavrasUnidas import DividePalavrasUnidas
from RemoveElementosDeMarcacao import RemoveElementosDeMarcacao
from TratamentoBasicoTexto import TratamentoBasicoTexto
from TratamentoDataEHora import TratamentoDataEHora
from TratamentoNumerico import TratamentoNumerico
from TratamentoTextoRedeSociais import TratamentoTextoRedeSociais
from TraducaoTexto import TraducaoTexto
from IdiomaTraducao import IdiomaTraducao

class TrataArquivos:
    def __init__(self, consolidaArquivos, tratamento, time_sleep_load_tratamento = 5, node_dest = 'text_tratado'):
        self.time_sleep_load_tratamento = time_sleep_load_tratamento
        self.consolidaArquivos = consolidaArquivos
        self.tratamento = tratamento
        self.node_dest = node_dest

    def tratar_arquivos(self, path, extension, tipo_arquivo, refazer_tratamento=False, propriedade_json = 'texto'):
        print('carregando lista de arquivos')
        file_list = self.consolidaArquivos.get_file_list(path, extension)
        self.tratar_arquivo(file_list, tipo_arquivo, refazer_tratamento, propriedade_json)

    def tratar_arquivo(self, file_list, tipo_arquivo, refazer_tratamento, propriedade_json):
        file_count = 0
        files_count_total = len(file_list)
        for file in file_list:
            file_count = file_count + 1
            print(f'Lendo arquivo: {file} posicao: {file_count} de: {files_count_total} faltam: {files_count_total - file_count}')
            content = self.consolidaArquivos.read_json(file)
            if tipo_arquivo == TipoDeArquivos.TWITTER:
                self.tratar_arquivos_twitter(file, content, refazer_tratamento, propriedade_json)
            elif tipo_arquivo == TipoDeArquivos.YOUTUBE_COMMENTS:
                self.tratar_arquivos_youtube(file, content, refazer_tratamento, propriedade_json)
            else:
                raise Exception(f'Função para enum: {tipo_arquivo} não implementada.')

    def tratar_arquivos_twitter(self, file, content, refazer_tratamento, propriedade_json):
        if self.node_dest in content and not refazer_tratamento:
            return
        print(f'processando arquivo: {file}')
        get_text_from_files = self.consolidaArquivos.get_text_from_twitter_json_files
        get_text_from_json = self.get_text_from_json_twitter
        set_text_from_json = self.set_text_from_json_twitter
        self.processa_tratamento_arquivos(file, content, get_text_from_files, get_text_from_json, set_text_from_json, propriedade_json)
    
    def tratar_arquivos_youtube(self, file, content, refazer_tratamento, propriedade_json):
        if self.node_dest in content and not refazer_tratamento:
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
        json[self.node_dest] = texto

    def set_text_from_json_youtube(self, json, texto):
        json[self.node_dest] = texto

    def processa_tratamento_arquivos(self, file, content, get_text_from_files, get_text_from_json, set_text_from_json, propriedade_json):
        json_content = get_text_from_files(content)
        texto = get_text_from_json(json_content, propriedade_json)

        texto_sem_emoji = self.resolve_tratamento_texto_ioc(texto)
        
        set_text_from_json(content, texto_sem_emoji)
        self.consolidaArquivos.save_json(file, content)
        time.sleep(self.time_sleep_load_tratamento)

    def resolve_tratamento_texto_ioc(self, texto):
        novo_texto = ''
        if type(self.tratamento ) is list:
            for classe_tratamento in self.tratamento:
                if type(classe_tratamento) is dict:
                    if classe_tratamento['Executar']:
                        print('Executando tratamento:', classe_tratamento['Classe'])
                        novo_texto = classe_tratamento['Classe'].tratar_texto(texto)
                    else:
                        print('Ignorando tratamento:', self.retorna_nome_classe(classe_tratamento['Classe']))
                        novo_texto = texto
                else:
                    print('Executando tratamento:', self.retorna_nome_classe(classe_tratamento))
                    novo_texto = classe_tratamento.tratar_texto(texto)
        else:
            print('Executando tratamento:', self.retorna_nome_classe(self.tratamento))
            novo_texto = self.tratamento.tratar_texto(texto)
        return novo_texto

    def retorna_nome_classe(self, classe):
        return type(classe).__name__

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

def test_tratar_arquivo_carrega_classe_tratar_arquivo_lst_texto_wordcloud():
    classe_tratamento_texto_wordcloud = [
        RemocaoDeUrl(),
        DividePalavrasUnidas(),
        CorrigiOrtografiaForaDoPadrao(),
        RemoveElementosDeMarcacao(),
        TratamentoBasicoTexto(False),
        TratamentoDataEHora(False),
        TratamentoTextoRedeSociais(False),
        TratamentoNumerico(False)
    ]
    consolidaArquivos = ConsolidaArquivos()
    trataArquivos = TrataArquivos(consolidaArquivos, classe_tratamento_texto_wordcloud, 0, 'texto_wordcloud')
    path_tweets = consolidaArquivos.PATH_TWEETS
    extension = consolidaArquivos.EXTENSION
    file_list = consolidaArquivos.get_file_list(path_tweets, extension)[0:10000]
    trataArquivos.tratar_arquivo(file_list, TipoDeArquivos.TWITTER, True, propriedade_json = "texto")

def tests():
    test_tratar_arquivo()
    test_tratar_arquivo_lst_classe_tratamento()
    test_lista_de_classes()

def carrega_classe_tratar_arquivo_lst(remocao_de_url = True, divide_palavras_unidas = True, corrigi_ortografia_fora_do_padrao = True, remove_elementos_de_marcacao = True, tratamento_basico_texto = True, tratamento_dataehora = True, tratamento_numerico = True, tratamento_texto_redesociais = True, usar_constante = True):
    classe_tratar_arquivo_lst = []
    if remocao_de_url:
        classe_tratar_arquivo_lst.append(RemocaoDeUrl())
    if divide_palavras_unidas:
        classe_tratar_arquivo_lst.append(DividePalavrasUnidas())
    if corrigi_ortografia_fora_do_padrao:
        classe_tratar_arquivo_lst.append(CorrigiOrtografiaForaDoPadrao())
    if remove_elementos_de_marcacao:
        classe_tratar_arquivo_lst.append(RemoveElementosDeMarcacao())
    if tratamento_basico_texto:
        classe_tratar_arquivo_lst.append(TratamentoBasicoTexto(usar_constante))
    if tratamento_dataehora:
        classe_tratar_arquivo_lst.append(TratamentoDataEHora(usar_constante))
    if tratamento_texto_redesociais:
        classe_tratar_arquivo_lst.append(TratamentoTextoRedeSociais(usar_constante))
    if tratamento_numerico:
        classe_tratar_arquivo_lst.append(TratamentoNumerico(usar_constante))
    return classe_tratar_arquivo_lst

def get_file_path_and_extension():
    consolidaArquivos = ConsolidaArquivos()
    path_tweets = consolidaArquivos.PATH_TWEETS
    path_youtube_comments = consolidaArquivos.PATH_YOUTUBE_COMMENTS
    extension = consolidaArquivos.EXTENSION
    return path_tweets, path_youtube_comments, extension, consolidaArquivos

def build_tratar_arquivos(consolidaArquivos: ConsolidaArquivos, ioc, path_tipo:Tuple, extension:str, time_sleep_load_tratamento:int = 0, node_dest:str = 'text_tratado', refazer_tratamento:bool=True, propriedade_json:str = 'texto_tratado'):
    path, tipo = path_tipo[0], path_tipo[1]
    trataArquivos = TrataArquivos(consolidaArquivos, ioc, time_sleep_load_tratamento, node_dest)
    trataArquivos.tratar_arquivos(path, extension, tipo, refazer_tratamento, propriedade_json)

def traduz_ingles(path_tweets, path_youtube_comments, extension, consolidaArquivos):
    traduzIngles = TraducaoTexto(Tradutor(), idioma=IdiomaTraducao.ENG, time_sleep=0)
    build_tratar_arquivos(consolidaArquivos=consolidaArquivos, ioc=traduzIngles, path_tipo=(path_tweets, TipoDeArquivos.TWITTER), extension=extension, time_sleep_load_tratamento=0, node_dest='texto_en', refazer_tratamento=False)
    build_tratar_arquivos(consolidaArquivos=consolidaArquivos, ioc=traduzIngles, path_tipo=(path_youtube_comments, TipoDeArquivos.YOUTUBE_COMMENTS),  extension=extension, time_sleep_load_tratamento=0, node_dest='texto_en', refazer_tratamento=False)

def verifica_idioma(path_tweets, path_youtube_comments, extension, consolidaArquivos):
    verificaIdioma = VerificaIdioma(Tradutor(), time_sleep=0)
    build_tratar_arquivos(consolidaArquivos, verificaIdioma, (path_tweets, TipoDeArquivos.TWITTER), extension, 0, 'idioma', refazer_tratamento=False, propriedade_json="texto")
    build_tratar_arquivos(consolidaArquivos, verificaIdioma, (path_youtube_comments, TipoDeArquivos.YOUTUBE_COMMENTS), extension, 0, 'idioma', refazer_tratamento=False, propriedade_json="texto")

def trata_texto(path_tweets, path_youtube_comments, extension, consolidaArquivos):
    classe_tratar_arquivo_lst = carrega_classe_tratar_arquivo_lst()
    build_tratar_arquivos(consolidaArquivos, classe_tratar_arquivo_lst, (path_tweets, TipoDeArquivos.TWITTER), extension, 0)
    build_tratar_arquivos(consolidaArquivos, classe_tratar_arquivo_lst, (path_youtube_comments, TipoDeArquivos.YOUTUBE_COMMENTS), extension, 0)

def trata_emoji(path_tweets, path_youtube_comments, extension, consolidaArquivos):
    trataEmoji = TrataEmoji(Tradutor(), time_sleep=0)
    build_tratar_arquivos(consolidaArquivos, trataEmoji, (path_tweets, TipoDeArquivos.TWITTER), extension, 0, propriedade_json = "texto")
    build_tratar_arquivos(consolidaArquivos, trataEmoji, (path_youtube_comments, TipoDeArquivos.YOUTUBE_COMMENTS), extension, 0, propriedade_json = "texto")

def trata_texto_wordcloud(path_tweets, path_youtube_comments, extension, consolidaArquivos):
    classe_tratamento_texto_wordcloud = carrega_classe_tratar_arquivo_lst(usar_constante=False)
    build_tratar_arquivos(consolidaArquivos, classe_tratamento_texto_wordcloud, (path_tweets, TipoDeArquivos.TWITTER), extension, 0, "texto_wordcloud", refazer_tratamento=True, propriedade_json = "texto")
    build_tratar_arquivos(consolidaArquivos, classe_tratamento_texto_wordcloud, (path_youtube_comments, TipoDeArquivos.YOUTUBE_COMMENTS), extension, 0, "texto_wordcloud", refazer_tratamento=True, propriedade_json = "texto")

def main():
    path_tweets, path_youtube_comments, extension, consolidaArquivos = get_file_path_and_extension()
    #trata_emoji(path_tweets, path_youtube_comments, extension, consolidaArquivos)
    #trata_texto(path_tweets, path_youtube_comments, extension, consolidaArquivos)
    #verifica_idioma(path_tweets, path_youtube_comments, extension, consolidaArquivos)
    #traduz_ingles(path_tweets, path_youtube_comments, extension, consolidaArquivos)
    trata_texto_wordcloud(path_tweets, path_youtube_comments, extension, consolidaArquivos)

if __name__ == '__main__':
    test_tratar_arquivo_carrega_classe_tratar_arquivo_lst_texto_wordcloud()