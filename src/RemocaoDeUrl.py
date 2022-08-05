import re
from typing import Final
import uuid

class RemocaoDeUrl:
    REMOVAL_OF_URLS_REGEX: Final[str] = r'https?:\/\/.*?[\s+]'
    STRING_TO_REPLACE_URL: Final[str] = ''
    def tratar_texto(self, texto):
        """
        Função que remove url de texto
        O parametro texto é o texto que será tratado
        """
        texto_com_espaco_em_branco = f"{texto} "
        novo_texto = ''
        match_lst = re.findall(self.REMOVAL_OF_URLS_REGEX, texto_com_espaco_em_branco)
        if match_lst:
            for match in match_lst:
                novo_texto = texto_com_espaco_em_branco.replace(match, self.STRING_TO_REPLACE_URL)
            return novo_texto[:-1]
        return texto

def main():
    url_lst = [
    'Desembargador declarou que as normas \"tornaram imposs\u00edvel o efetivo cuidado com a sa\u00fade p\u00fablica\"',
    'http://www.youtube.com/watch?v=qsXHcwe3krw', 
    'http://41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg', 
    'enfp and intj moments https://www.youtube.com/watch?v=iz7lE1g4XM4 sportscenter not ', 
    'top ten plays https://www.youtube.com/watch?v=uCdfze1etec pranks', 
    'Desembargador declarou que as normas \"tornaram imposs\u00edvel o efetivo cuidado com a sa\u00fade p\u00fablica\" ==&gt; https://t.co/aDgqkf1rIU #g1RO',
    'Origem misteriosa? Do que \u00e9 feita:\nCada dose (0,5 ml) cont\u00e9m: adenov\u00edrus tipo 26 que codifica a glicoprote\u00edna S (spike*) do SARS-CoV-2 (Ad26.COV2-S), n\u00e3o inferior a 8,92 log10 unidades infecciosas (U.Inf.). da J&J\nhttps://t.co/hZmG3IP8pu',
    '@passistagotica \u00e9 bem f\u00e1cil\nvai no app conecte sus depois \nvacinas>covid-19>certificado de vacina\u00e7\u00e3o>adicionar no wallet https://t.co/fRnQEYltUV',
    "Desembargador"]
    remocaoDeUrl = RemocaoDeUrl()
    for url in url_lst:
        texto_sem_url = remocaoDeUrl.tratar_texto(url)
        print('texto_sem_url:', texto_sem_url)

if __name__ == '__main__':
    main()

