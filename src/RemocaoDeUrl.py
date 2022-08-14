import re
from typing import Final
from TratamentoTextoBase import TratamentoTextoBase

class RemocaoDeUrl(TratamentoTextoBase):
    REMOVAL_OF_URLS_REGEX: Final[str] = r'(htt?p?s?:\/?\/.*?[\s+])|(htt?p?s?:?.*[\s+])'
    STRING_TO_REPLACE_URL: Final[str] = ''

    def remove_urls(self, transient_tweet_text):
        texto_com_espaco_em_branco = f"{transient_tweet_text} "
        return re.sub(self.REMOVAL_OF_URLS_REGEX, self.STRING_TO_REPLACE_URL, texto_com_espaco_em_branco)[:-1]
        
    def tratar_texto(self, texto):
        """
        Função que remove url de texto
        O parametro texto é o texto que será tratado
        """
        texto = self.to_lowercase(texto)
        texto = self.remove_urls(texto)
        return texto

def main():
    textos = [
    'Desembargador declarou que as normas \"tornaram imposs\u00edvel o efetivo cuidado com a sa\u00fade p\u00fablica\"',
    'http://www.youtube.com/watch?v=qsXHcwe3krw', 
    'http://41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg', 
    'enfp and intj moments https://www.youtube.com/watch?v=iz7lE1g4XM4 sportscenter not ', 
    'top ten plays https://www.youtube.com/watch?v=uCdfze1etec pranks', 
    'Desembargador declarou que as normas \"tornaram imposs\u00edvel o efetivo cuidado com a sa\u00fade p\u00fablica\" ==&gt; https://t.co/aDgqkf1rIU #g1RO',
    'Origem misteriosa? Do que \u00e9 feita:\nCada dose (0,5 ml) cont\u00e9m: adenov\u00edrus tipo 26 que codifica a glicoprote\u00edna S (spike*) do SARS-CoV-2 (Ad26.COV2-S), n\u00e3o inferior a 8,92 log10 unidades infecciosas (U.Inf.). da J&J\nhttps://t.co/hZmG3IP8pu',
    '@passistagotica \u00e9 bem f\u00e1cil\nvai no app conecte sus depois \nvacinas>covid-19>certificado de vacina\u00e7\u00e3o>adicionar no wallet https://t.co/fRnQEYltUV',
    "Desembargador",
    "este e o primeiro tratamento incluido no sistema unico de saude (sus) para tratar os pacientes contra o virus.\n#tvcultura #covid #sus\nhttps://t.co/",
    "Este é o primeiro tratamento incluído no Sistema Único de Saúde (SUS) para tratar os pacientes contra o vírus.\n#TVCultura #Covid #SUS\nhttps://t.co/JxsA7e1SxB",
    "este e o primeiro tratamento incluido no sistema unico de saude (sus) para tratar os pacientes contra o virus.\n#tvcultura #covid #sus\nhttps://t.co/",
    "pernambuco esta sob o alerta ha mais de dois anos.\nhttps://t.co/ ",
    "consulta publica para incorporacao pelo sus dos imunobiologicos tixagevimabe e cilgavimabe. >participe: htps:/t.co/                         ",
    "Sobre pandemias, ci\u00eancia(s) e cuidado: desafios da Sa\u00fade Coletiva e do Sistema \u00danico de Sa\u00fade (SUS) para a inven\u00e7\u00e3o de uma vida outra - S\u00e9rgio Resende Carvalho\n\nAcesso em: https://t.co/PxAFf29GTl\n\n#pandemia #SUS #saudecoletiva https://t.co/QLyRUcI9qs",
    "rt @ciencia_sou: sao perguntas importantes e para as quais nao temos respostas definitivas.  saiba mais no blog do sou_c na @folha: https:...",
    "rt @ : eua assinou um contrato para \"pesquisa covid \" na ucrania   meses antes de se tornar conhecida a existencia covid...\nhttps..."
    ]
    remocaoDeUrl = RemocaoDeUrl()
    for texto in textos:
        print("-------------------------------------------------------------------------------------")
        print("antes:", texto)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("depois:", remocaoDeUrl.tratar_texto(texto))
        print("-------------------------------------------------------------------------------------")

if __name__ == '__main__':
    main()

