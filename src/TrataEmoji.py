from genericpath import exists
import json
from typing import Final
import demoji
import uuid
from Tradutor import Tradutor
import time

"""
Links:
https://acervolima.com/converta-emoji-em-texto-em-python/
https://pypi.org/project/demoji/

"""

class TrataEmoji:
    FULL_PATH_FILE_DICT_EMOJI: Final[str] = f'data/dict_emoji.json'

    def __init__(self, tradutor, time_sleep = 5):
        self.tradutor = tradutor
        self.time_sleep = time_sleep

    def retorna_dict_emoji_texto(self, texto):
        '''Função que retorno um dicionário de emoji e o respectivo texto'''
        return demoji.findall(texto)

    def converte_emoji_em_texto(self, texto, sep=" "):
        '''
        Função que converte emoji em texto
        O parametro texto é o texto utilizado para converter os emojis em texto
        O parametro sep é o texto utilizado para separar os emojis do texto
        '''
        return demoji.replace_with_desc(texto, sep)

    def retorna_lista_emoji_do_texto(self, texto):
        '''
        Função que retorna lista de emojis de uma string
        O parametro texto é o texto utilizado para converter os emojis em texto
        '''
        return demoji.findall_list(texto)

    def traduz_emojis_ptbr(self, emojis):
        '''
        Função que traduz emojis para portugues
        O parametro texto é o texto utilizado para converter os emojis em texto
        '''
        emojis_iteration = emojis
        if isinstance(emojis, dict):
            emojis_iteration = emojis.values()
        emojis_traduzidos = []
        for emoji in emojis_iteration:
            emojis_traduzidos.append(self.tradutor.traducao_portugues(emoji))
            time.sleep(self.time_sleep)
        return emojis_traduzidos

    def cria_dicionario_traducao_emoji(self, emojis, emojis_traduzidos):
        '''
        Função que cria dicionário de tradução de emoji
        O parametro emojis é a lista de emojis original
        O parametro emojis_traduzidos é a lista de emojis traduzidos
        '''
        emojis_iteration = emojis
        emojis_traduzidos_iteration = emojis_traduzidos
        if isinstance(emojis, dict):
            emojis_iteration = emojis.values()
        if isinstance(emojis_traduzidos, dict):
            emojis_traduzidos_iteration = emojis_traduzidos.values()

        list_dict_emoji = []
        for emoji, emoji_traduzido in zip(emojis_iteration, emojis_traduzidos_iteration):
            list_dict_emoji.append({
                'original_text': emoji, 
                'translated_text': emoji_traduzido})
        return list_dict_emoji
    
    def converte_traduz_emoji_em_texto(self, texto, usar_dicionario_emoji = True, atualizar_dicionario_emoji = False, start_sep = "(", end_sep = ")"):
        '''
        Função que traduz emoji em texto
        O parametro texto é o texto a ser traduzido
        O parametro usar_dicionario_emoji utiliza dicionario emoji com as traduções já feitas e atualiza caso não existir
        O parametro atualizar_dicionario_emoji substitui dicionário emoji traduzindo novamente cada emoji
        O parametro start_sep separador a ser adicionado no inicio da tradução do emoji
        O parametro end_sep separador a ser adicionado no final da tradução do emoji
        '''
        list_dict_emoji = self.retorna_lista_dicionario_emoji_traduzido(texto, usar_dicionario_emoji, atualizar_dicionario_emoji)
        id_tag = f"<:{str(uuid.uuid4())}:>"
        texto_sem_emoji = self.converte_emoji_em_texto(texto, id_tag)
        for emoji in list_dict_emoji:
            old_string = f"{id_tag}{emoji['original_text']}{id_tag}"
            new_string = f"{start_sep}{emoji['translated_text']}{end_sep}"
            texto_sem_emoji = texto_sem_emoji.replace(old_string, new_string)
        return texto_sem_emoji

    def retorna_lista_dicionario_emoji_traduzido(self, texto, usar_dicionario_emoji = True, atualizar_dicionario_emoji = False):
        '''
        Função que retorna a lista de dicionário de emojis traduzidos de um texto
        O parametro texto é o texto a ser traduzido
        O parametro usar_dicionario_emoji utiliza dicionario emoji com as traduções já feitas e atualiza caso não existir
        '''
        emojis_traduzidos = []
        emojis_dict = self.retorna_dict_emoji_texto(texto)
        if usar_dicionario_emoji:
            emojis_traduzidos = self.retorna_emojis_dicionario(emojis_dict)
        if not emojis_traduzidos:
            emojis_traduzidos = self.traduz_emojis_ptbr(emojis_dict)
        list_dict_emoji = self.cria_dicionario_traducao_emoji(emojis_dict, emojis_traduzidos)
        if usar_dicionario_emoji:
            self.salvar_emojis_dicionario(emojis_dict, list_dict_emoji, atualizar_dicionario_emoji)
        return list_dict_emoji

    def retorna_emojis_dicionario(self, emojis_dict):
        '''
        Função que retorna a lista de emojis do dicionário de emojis
        O parametro emojis_dict são os emojis a serem buscados no dicionário
        '''
        emojis_encontrados_no_dicionario = []
        json = self.read_json(self.FULL_PATH_FILE_DICT_EMOJI)
        for emoji in emojis_dict:
            json_emoji = next((dict_emoji for dict_emoji in json if emoji in dict_emoji), None)
            if json and json_emoji:
                translated_text = list(json_emoji.values())[0]['translated_text']
                emojis_encontrados_no_dicionario.append(translated_text)
        return emojis_encontrados_no_dicionario

    def verifica_emoji_dicionario_emoji(self, emoji, json):
        '''
        Função que verifica se emoji existe no dicionário de emojis
        O parametro emoji são os emojis do texto
        O parametro json dicionário de emojis
        '''
        emoji_no_dicionario = False
        for emoji_dict in json:
            if emoji in emoji_dict:
                emoji_no_dicionario = True
                break
        return emoji_no_dicionario

    def salvar_emojis_dicionario(self, emojis_dict, list_dict_emoji, atualizar_dicionario_emoji = False):
        '''
        Função que salva emoji no dicionário de emojis
        O parametro emojis_dict são os emojis do texto
        O parametro list_dict_emoji são os emojis traduzidos e descritos do texto
        O parametro atualizar_dicionario_emoji força a atualização do dicionario de emoji
        '''
        json = self.read_json(self.FULL_PATH_FILE_DICT_EMOJI)
        lst_new_dict_emoji = json
        for emoji, dict_emoji in zip(emojis_dict, list_dict_emoji):
            if not self.verifica_emoji_dicionario_emoji(emoji, json) or atualizar_dicionario_emoji:
                lst_new_dict_emoji.append({ emoji: dict_emoji })
        self.save_json(self.FULL_PATH_FILE_DICT_EMOJI, lst_new_dict_emoji)

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
            try:
                content = json.load(f)
            except ValueError:
                return content
        return content

    def tratar_texto(self, texto, usar_dicionario_emoji = False):
        return self.converte_traduz_emoji_em_texto(texto, usar_dicionario_emoji)

#Teste
def test_converte_texto_em_emoji():
  '''Função que testa a função converte_texto_em_emoji'''
  tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
  trataEmoji = TrataEmoji(Tradutor())
  tweet_sem_emoji = trataEmoji.converte_emoji_em_texto(tweet, ' ')
  print(tweet_sem_emoji)

def test_converte_traduz_emoji_em_texto():
    '''Função que testa a função converte_traduz_emoji_em_texto'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    tweet_sem_emoji = trataEmoji.converte_traduz_emoji_em_texto(tweet)
    print(tweet_sem_emoji)

def test_retorna_lista_emoji_do_texto():
    '''Função que testa a função retorna_lista_emoji_do_texto'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    print(trataEmoji.retorna_lista_emoji_do_texto(tweet))

def test_retorna_dict_emoji_texto():
    '''Função que testa a função retorna_dict_emoji_texto'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    print(trataEmoji.retorna_dict_emoji_texto(tweet))

def test_retorna_lista_dicionario_emoji_traduzido():
    '''Função que testa a função retorna_lista_dicionario_emoji_traduzido'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    print(trataEmoji.retorna_lista_dicionario_emoji_traduzido(tweet))

def test_retorna_emojis_dicionario():
    '''Função que testa a função retorna_emojis_dicionario'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    emojis_dict = trataEmoji.retorna_dict_emoji_texto(tweet)
    print(trataEmoji.retorna_emojis_dicionario(emojis_dict))

def test_salvar_emojis_dicionario():
    '''Função que testa a função salvar_emojis_dicionario'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    emojis_traduzidos = []
    
    emojis_dict = trataEmoji.retorna_dict_emoji_texto(tweet)
    emojis_traduzidos = trataEmoji.traduz_emojis_ptbr(emojis_dict)
    list_dict_emoji = trataEmoji.cria_dicionario_traducao_emoji(emojis_dict, emojis_traduzidos)
    trataEmoji.salvar_emojis_dicionario(emojis_dict, list_dict_emoji)

def test_salvar_emojis_dicionario_texto_sem_emoji():
    '''Função que testa a função salvar_emojis_dicionario'''
    tweet = "#startspreadingthenews yankees win great start by going 5strong innings with 5k’s"
    trataEmoji = TrataEmoji(Tradutor())
    emojis_traduzidos = []
    
    emojis_dict = trataEmoji.retorna_dict_emoji_texto(tweet)
    emojis_traduzidos = trataEmoji.traduz_emojis_ptbr(emojis_dict)
    list_dict_emoji = trataEmoji.cria_dicionario_traducao_emoji(emojis_dict, emojis_traduzidos)
    trataEmoji.salvar_emojis_dicionario(emojis_dict, list_dict_emoji)

def test_tratar_texto():
    '''Função que testa a função tratar_texto'''
    tweet = "#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂"
    trataEmoji = TrataEmoji(Tradutor())
    print(trataEmoji.tratar_texto(tweet))

def main():
    test_converte_texto_em_emoji()
    test_converte_traduz_emoji_em_texto()
    test_retorna_lista_emoji_do_texto()
    test_retorna_dict_emoji_texto()
    test_retorna_lista_dicionario_emoji_traduzido()
    test_retorna_emojis_dicionario()
    test_salvar_emojis_dicionario()
    test_salvar_emojis_dicionario_texto_sem_emoji()
    test_tratar_texto()

if __name__ == '__main__':
    main()