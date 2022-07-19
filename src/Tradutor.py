from googletrans import Translator, LANGCODES


class Tradutor:
    def __init__(self):
        self.translator = Translator()

    def traducao_portugues(self, texto):
        """
        Função que traduz o texto para portugues usando o google tradutor
        O parametro texto será o texto a ser traduzido para portugues
        returna a tradução
        """
        sigla_portugues = LANGCODES['portuguese']
        return self.translator.translate(texto, dest=sigla_portugues).text


def test_traducao_portugues():
    tradutor = Tradutor()
    texto = '안녕하세요.'
    print(tradutor.traducao_portugues(texto))

def main():
    test_traducao_portugues()

if __name__ == '__main__':
    main()