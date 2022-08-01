from bs4 import BeautifulSoup

class RemoveElementosDeMarcacao:
    def tratar_texto(self, texto):
        """
        Função que trata o texto removendo os elementos de marcação
        O parametro texto é o texto que será tratado
        Esse código foi baseado no código da bibliografia:
        Vajjala, S. et al. Practical Natural Language Processing. 1 ed. Sebastopol, CA: O'Reilly Media, 2020.
        tópico: Removing markup elements página 293
        """
        soup = BeautifulSoup(texto, features="html.parser")
        return soup.get_text()

def main():
    texto = '<a href="http://nlp.cpm/">\nI love <i>nlp</i>\n</a>'
    removeElementosDeMarcacao = RemoveElementosDeMarcacao()
    textoSemElementosDeMarcacao = removeElementosDeMarcacao.tratar_texto(texto)
    print("textoSemElementosDeMarcacao:", textoSemElementosDeMarcacao)

if __name__ == '__main__':
    main()