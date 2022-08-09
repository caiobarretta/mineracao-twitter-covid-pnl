from typing import Final
from unidecode import unidecode

class TratamentoTextoBase:
    BLANK_SPACE: Final[str] = ' '
    def __init__(self, usar_constante=True):
        self.usar_constante = usar_constante
    def regex_or(self, *items):
        r = '|'.join(items)
        r = '(' + r + ')'
        return r
        
    def strip_unicode(self, transient_tweet_text):
        '''
        Trata caracteres unicode
        '''
        return unidecode(transient_tweet_text)
        
    def to_lowercase(self, transient_tweet_text):
        '''
        Convert tweet text to lower to lower case alphabets
        '''
        transient_tweet_text = transient_tweet_text.lower()
        return transient_tweet_text

    def verifica_utilizacao_contantes(self, constante):
        if self.usar_constante:
            return constante
        return self.BLANK_SPACE

def test_strip_unicode():
    tratamento = TratamentoTextoBase()
    textos = [
        "@DefesaGovBr Orientafos n\u00e3o s\u00f3 a atacar o processo eleitoral  e tamb\u00e9m seu pr\u00f3prio povo. A exemplo dos hospitais mi\u2026",
        "RT @jairbolsonaro: - O @minsaude converte 6,4 mil leitos de unidade de terapia intensiva (UTI) exclusivos para covid em leitos convencionai\u2026",
        "RT @LulaOficial: O SUS sempre foi muito atacado, principalmente pela iniciativa privada. Na pandemia, se n\u00e3o fosse o SUS, ter\u00edamos mais de\u2026",
        "RT @outrasaude: Leia as principais not\u00edcias de Sa\u00fade de hoje, em apenas dez minutos #outrasaude\n",
    ]
    for texto in textos:
        texto_sem_unicode = tratamento.strip_unicode(texto)
        print("texto:", texto)
        print("texto_sem_unicode:", texto_sem_unicode)

def main():
    test_strip_unicode()

if __name__ == '__main__':
    main()
