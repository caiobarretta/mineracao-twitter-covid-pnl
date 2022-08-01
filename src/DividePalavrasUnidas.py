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
        return " ".join(re.findall(self.SPLIT_JOINED_REGEX, texto))

def main():
    texto = "BomDia"
    dividePalavrasUnidas = DividePalavrasUnidas()
    textoSemPalavrasUnidas = dividePalavrasUnidas.tratar_texto(texto)
    print('textoSemPalavrasUnidas:', textoSemPalavrasUnidas)

if __name__ == '__main__':
    main()