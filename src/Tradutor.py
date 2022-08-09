from googletrans import Translator, LANGCODES
from typing import Final
import time

class Tradutor:
    SIGLA_PORTUGUES: Final[str] = LANGCODES['portuguese']
    SIGLA_INGLES: Final[str] = LANGCODES['english']
    def __init__(self, numero_tentivas_maximo = 10,  time_sleep_tentativas = 2):
        self.translator = Translator()
        self.numero_tentivas_maximo = numero_tentivas_maximo
        self.time_sleep_tentativas = time_sleep_tentativas

    def call_translate(self, texto, dest):
        """
        Função que chama a tradução do texto  usando o google tradutor
        O parametro texto será o texto a ser traduzido
        returna o texto traduzido
        """
        retorno_translator = ''
        numero_tentativas = 0
        while(numero_tentativas < self.numero_tentivas_maximo):
            try:
                retorno_translator = self.translator.translate(texto, dest=dest).text
                print(f'Traduzido na tentativa número: {numero_tentativas + 1}')
                break
            except:
                numero_tentativas = numero_tentativas + 1
                if self.time_sleep_tentativas == 0:
                    time.sleep(numero_tentativas)
                time.sleep(self.time_sleep_tentativas)
        if numero_tentativas >= self.numero_tentivas_maximo:
            raise Exception(f'Ocorreu um erro ao tentar traduzir o texto: {texto} para a língua: {dest} Número de tentativas: {numero_tentativas}')
        return retorno_translator

    def traducao_portugues(self, texto):
        """
        Função que traduz o texto para portugues usando o google tradutor
        O parametro texto será o texto a ser traduzido para portugues
        returna a tradução
        """
        return self.call_translate(texto, dest=self.SIGLA_PORTUGUES)

    def traducao_ingles(self, texto):
        """
        Função que traduz o texto para inglês usando o google tradutor
        O parametro texto será o texto a ser traduzido para inglês
        returna a tradução
        """
        return self.call_translate(texto, dest=self.SIGLA_INGLES)

    def verifica_idioma(self, texto):
        """
        Função que verifica o idioma do texto usando o google tradutor
        O parametro texto será o texto a ser verificado
        returna o idioma
        """
        retorno_translator = ''
        numero_tentativas = 0
        while(numero_tentativas < self.numero_tentivas_maximo):
            try:
                retorno_translator = self.translator.detect(texto).lang
                break
            except:
                numero_tentativas = numero_tentativas + 1
                time.sleep(self.time_sleep_tentativas)
        if numero_tentativas >= self.numero_tentivas_maximo:
            raise Exception(f'Ocorreu um erro ao tentar traduzir o texto: {texto} Número de tentativas: {numero_tentativas}')
        return retorno_translator


def test_traducao_portugues():
    tradutor = Tradutor(1, 1)
    texto = '안녕하세요.'
    print('Tradução Português')
    print('texto:', texto)
    print('tradução:', tradutor.traducao_portugues(texto))


def test_traducao_ingles():
    tradutor = Tradutor(1, 1)
    texto = '안녕하세요.'
    print('Tradução Inglês')
    print('texto:', texto)
    print('tradução:', tradutor.traducao_ingles(texto))

def test_verifica_idioma():
    tradutor = Tradutor(1, 1)
    textos = [
        "Excelente MESTRE Peninha !!!!\nO nosso maior problema em todas as 00e1reas 00e9 a corrup00e700e3o, no SUS agora o COVID00c3O, enquanto os miser00e1veis morrem nos hospitais p00fablicos os de sempre continuam roubando.\nVoc00ea j00e1 fez algum cap00edtulo da CORRUP00c700c3O NO BRASIL  ?\nd83dde4fd83dde4fd83dde4fd83dde4f",
        "Una gran informaci00f3n y es una gran preocupaci00f3n hasta donde llega la ignorancia de las personas  al desechar todas sus basuras a los r00edos y mares no tomando en cuenta que estamos cavando nuestra propia tumba  al esparcir todos estos virus en  lo que nos da la vida, el agua, de verdad es muy preocupante ver los r00edos infestados de cubre bocas  y basura desechos de toda esta pandemia.  Saludos y muchas felicidades por su valiosa informaci00f3n.",
        "O que mais me assusta, 00e9 que minha irm00e3, n00e3o sai de casa, fica 24 horas dentro de casa, foi fazer o teste do covid conforme todo mundo foi, e l00e1 no hospital de campanha trocaram o nome dela, e quando fez o teste deu positivo, sem sintomas algum, minha m00e3e queria pagar um particular, falei: Pra que pagar? se nem de casa ela sai, minha irm00e3 tem 14 anos. dai ficou por isso mesmo.\nOutro caso 00e9 da minha cunhada, no laborat00f3rio particular o teste deu negativo, j00e1 no p00fablico deu positivo. :/\n\nO MP, deviam investigar direito isso, em vez de estarem preocupados em prender os pais que n00e3o vacinarem os filhos.\n\nno interior de SP, um caso recente de uma crian00e7a que tomou a vacina infantio, e 12 horas depois teve um infarto. Devido a isso nessa cidade suspenderam a vacina00e700e3o, e nas demais cidades n00e3o suspenderam.",
        "Semoga vurus corona segera pergi dari dunia ini,khususnya negara kita(indonesia)AAMIINd83edd32"
        ]
    print('Verificação de idioma.')
    for texto in textos:
        idioma = tradutor.verifica_idioma(texto)
        print("idioma: ", idioma)
        print("texto:", texto)

def main():
    test_traducao_portugues()
    test_traducao_ingles()
    test_verifica_idioma()

if __name__ == '__main__':
    main()