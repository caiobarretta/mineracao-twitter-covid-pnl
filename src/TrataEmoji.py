import demoji
import uuid
from Tradutor import Tradutor

"""
Links:
https://acervolima.com/converta-emoji-em-texto-em-python/
https://pypi.org/project/demoji/

"""

class TrataEmoji:
    def __init__(self, tradutor):
        self.tradutor = tradutor

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
        emojis_traduzidos = []
        for emoji in emojis:
            emojis_traduzidos.append(self.tradutor.traducao_portugues(emoji))
        return emojis_traduzidos

    def cria_dicionario_traducao_emoji(self, emojis, emojis_traduzidos):
        '''
        Função que cria dicionário de tradução de emoji
        O parametro emojis é a lista de emojis original
        O parametro emojis_traduzidos é a lista de emojis traduzidos
        '''
        list_dict_emoji = []
        for emoji, emoji_traduzido in zip(emojis, emojis_traduzidos):
            list_dict_emoji.append({
                'original_text': emoji, 
                'translated_text': emoji_traduzido})
        return list_dict_emoji
    
    def converte_traduz_emoji_em_texto(self, texto, start_sep = "(", end_sep = ")"):
        emojis = self.retorna_lista_emoji_do_texto(texto)
        emojis_traduzidos = self.traduz_emojis_ptbr(emojis)
        list_dict_emoji = self.cria_dicionario_traducao_emoji(emojis, emojis_traduzidos)
        
        id_tag = f"<:{str(uuid.uuid4())}:>"
        texto_sem_emoji = self.converte_emoji_em_texto(texto, id_tag)
        for emoji in list_dict_emoji:
            old_string = f"{id_tag}{emoji['original_text']}{id_tag}"
            new_string = f"{start_sep}{emoji['translated_text']}{end_sep}"
            texto_sem_emoji = texto_sem_emoji.replace(old_string, new_string)
        return texto_sem_emoji

    def tratar_texto(self, texto):
        return self.converte_traduz_emoji_em_texto(texto)

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

def main():
    test_converte_texto_em_emoji()
    test_converte_traduz_emoji_em_texto()

if __name__ == '__main__':
    main()