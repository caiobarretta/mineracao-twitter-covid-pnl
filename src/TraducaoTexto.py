import time
from Tradutor import Tradutor
from IdiomaTraducao import IdiomaTraducao

class TraducaoTexto:
    def __init__(self, tradutor: Tradutor, idioma:IdiomaTraducao, time_sleep:int = 5):
        self.tradutor = tradutor
        self.idioma = idioma
        self.time_sleep = time_sleep

    def tratar_texto(self, texto):
        time.sleep(self.time_sleep)
        if self.idioma == IdiomaTraducao.PT:
            return self.tradutor.traducao_portugues(texto)
        if self.idioma == IdiomaTraducao.ENG:
            return self.tradutor.traducao_ingles(texto)
        else:
            raise Exception("Traducao de lingua não implementada.")