import re
from typing import Final

class DividePalavrasUnidas:
    SPLIT_JOINED_REGEX: Final[str] = '[A-Z][^A-Z]*'

    def tratar_texto(self, texto):
        """
        Função que trata o texto que possuem palavras unidas
        O parametro texto é o texto que será tratado
        Esse código foi baseado no código da bibliografia:
        Vajjala, S. et al. Practical Natural Language Processing. 1 ed. Sebastopol, CA: O'Reilly Media, 2020.
        tópico: Split-joined words página 295
        """
        joined_string = " ".join(re.findall(self.SPLIT_JOINED_REGEX, texto))
        if not joined_string:
            return texto
        return joined_string

def main():
    textos = [
        "BomDia",
        "Texto correto",
        "TesteTexto com texto normal ",
        "TesteTexto com texto normal",
        "@defesagovbr","orientafos","nao","so","a","atacar","o","processo","eleitoral","","e","tambem","seu","proprio","povo.","a","exemplo","dos","hospitais","mi...","https://t.co/","",
        ]
    dividePalavrasUnidas = DividePalavrasUnidas()
    for texto in textos:
        print("-------------------------------------------------------------------------------------")
        print("antes:", texto)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("depois:", "'"+dividePalavrasUnidas.tratar_texto(texto)+"'")
        print("-------------------------------------------------------------------------------------")
if __name__ == '__main__':
    main()