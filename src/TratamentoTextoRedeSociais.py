import re
from typing import Final
from TratamentoTextoBase import TratamentoTextoBase

class TratamentoTextoRedeSociais(TratamentoTextoBase):
    PROCESS_MENTIONS_REGEX: Final[str] = r"@(\w+)"
    PROCESS_MENTIONS_WITH_PUNCTUATION_REGEX: Final[str] = r'@\w+[.?\-",]\w+'
    PROCESS_MENTIONS_WITH_PUNCTUATION_TWICE_REGEX: Final[str] = r'@\w+[.?\-",]\w+[.?\-",]\w+'
    CONSTANT_NON_BRAND_MENTION: Final[str] = " constante_nao_mencao_da_marca "

    PROCESS_HASHTAGS_REGEX: Final[str] = r"#(\w+)\b"
    CONSTANT_HASHTAG: Final[str] = " hashtag_constante "

    REMOVE_RETWEET: Final[str] = r'(rt )|( rt )|( rt)'

    def __init__(self, usar_constante=True):
        super(TratamentoTextoRedeSociais, self).__init__(usar_constante)

    def tratar_texto(self, texto):
        texto = self.strip_unicode(texto)
        texto = self.to_lowercase(texto)
        texto = self.process_hashtags(texto)
        texto = self.process_mentions_with_punctuation_twice(texto)
        texto = self.process_mentions_with_punctuation(texto)
        texto = self.process_mentions(texto)
        texto = self.remove_retweet(texto)
        return texto

    def process_mentions(self, transient_tweet_text):
        '''
        Identify mentions if any
        '''
        return re.sub(self.PROCESS_MENTIONS_REGEX, self.verifica_utilizacao_contantes(self.CONSTANT_NON_BRAND_MENTION), transient_tweet_text)

    def process_mentions_with_punctuation_twice(self, transient_tweet_text):
        '''
        Identify mentions if any
        '''
        return re.sub(self.PROCESS_MENTIONS_WITH_PUNCTUATION_TWICE_REGEX, self.verifica_utilizacao_contantes(self.CONSTANT_NON_BRAND_MENTION), transient_tweet_text)

    def process_mentions_with_punctuation(self, transient_tweet_text):
        '''
        Identify mentions if any
        '''
        return re.sub(self.PROCESS_MENTIONS_WITH_PUNCTUATION_REGEX, self.verifica_utilizacao_contantes(self.CONSTANT_NON_BRAND_MENTION), transient_tweet_text)

    def process_hashtags(self, transient_tweet_text):
        '''
        Strip all Hashtags from a tweet
        '''
        return re.sub(self.PROCESS_HASHTAGS_REGEX, self.verifica_utilizacao_contantes(self.CONSTANT_HASHTAG), transient_tweet_text)

    def remove_retweet(self, transient_tweet_text):
        '''
        Remove a marcação RT (retweet)
        '''
        return re.sub(self.REMOVE_RETWEET, self.BLANK_SPACE, transient_tweet_text)

def test_trata_texto():
    textos = [
        "Nice @varun paytm @paytm saver rtabc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)",
        "rt @tali_mito22: o descondenado e sua canjinha estao com covid.rt detalhe, ele tem  constante_numerica  doses de vachina e sua canja  constante_numerica  doses.\nagora a pergunta:... rt",
        "rt @jaqueswagner: testei positivo para a covid  nesta segunda-feira ( ). estou bem, com sintomas leves e isolado em casa, em salvador. f...",
        "Medicamentos antivirais para Covid-19 s\u00e3o inclu\u00eddos pelo SUS; veja como funciona: Os medicamentos para Covid-19 t\u00eam o potencial de reduzir o risco de complica\u00e7\u00f5es da doen\u00e7a. Os\u2026 https://t.co/8zop05vagw @jcconcursos.com.br @jcconcursos.com.br #concursos #empregos #edital https://t.co/mVgac4zMHF",
        "@teste.com @teste.com.br"
    ]
    tratamento = TratamentoTextoRedeSociais()

    for texto in textos:
        print("-------------------------------------------------------------------------------------")
        print("antes:", texto)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("depois:", tratamento.tratar_texto(texto))
        print("-------------------------------------------------------------------------------------")

def main():
    test_trata_texto()

if __name__ == '__main__':
    main()