import re
from typing import Final

class CorrigiOrtografiaForaDoPadrao:
    NONSTANDARD_SPELLINGS_REGEX_PATTERN: Final[str] = r'(.)\1+'
    NONSTANDARD_SPELLINGS_REGEX_REPL: Final[str] = r'\1'
    def tratar_texto(self, texto):
        """
        Função que corrigi ortografia fora do padrao
        O parametro texto é o texto que será tratado
        Esse código foi baseado no código da bibliografia:
        Vajjala, S. et al. Practical Natural Language Processing. 1 ed. Sebastopol, CA: O'Reilly Media, 2020.
        tópico: Nonstandard spellings página 295
        """
        return re.sub(self.NONSTANDARD_SPELLINGS_REGEX_PATTERN, self.NONSTANDARD_SPELLINGS_REGEX_REPL, texto)

def main():
    textos = ["Siiiiimmmmmmmm ", "oooooooooooooooooooooooooooiiiiiiii ", "Viiiishhhhhiiiiiiii "]
    corrigiOrtografiaForaDoPadrao = CorrigiOrtografiaForaDoPadrao()
    for texto in textos:
        textoComCorrecaoDeOrtografiaForaDoPadrao = corrigiOrtografiaForaDoPadrao.tratar_texto(texto)
        print('textoComCorrecaoDeOrtografiaForaDoPadrao:', textoComCorrecaoDeOrtografiaForaDoPadrao)

if __name__ == '__main__':
    main()