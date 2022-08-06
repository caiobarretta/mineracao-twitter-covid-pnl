import re
from typing import Final
from TratamentoTextoBase import TratamentoTextoBase

class TratamentoDataEHora(TratamentoTextoBase):
    CONSTANT_DATE: Final[str] = ' constantedata '
    CONSTANT_TIME: Final[str] = ' constantetempo '

    DATE_REGEX_EN1: Final[str] = r'\b((0|1|2|3)?[0-9][\s]*)[-./]([\s]*([012]?[0-9])[\s]*)([-./]([\s]*(19|20)[0-9][0-9]))?\b'
    DATE_REGEX_EN2: Final[str] = r'\b((19|20)[0-9][0-9][\s]*[-./]?)?[\s]*([012]?[0-9])[\s]*[-./][\s]*(0|1|2|3)?[0-9]\b'
    DATE_REGEX_EN3: Final[str] = r'\d+[\s]*(st|nd|rd|th)[\s]*'
    DATE_REGEX_EN4: Final[str] = r'[\s]*\d+[\s]*(st|nd|rd|th)*\b'
    DATE_REGEX_EN5: Final[str] = r'[\s]?\b(19|20)[0-9][0-9]\b[\s]?'
    DATE_REGEX_EN6: Final[str] = r'([\s]*(constantedata))+'
    TIME_REGEX: Final[str] = r'([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9][\s]*(am|pm)?[\s]*([iescm](st)|gmt|utc|[pmce](dt))?'

    DATE_REGEX_PTBR1: Final[str] = r'(0[1-9]|1\d{1}|2\d{1}|3[0-1])(\/|\-|\.)(0[1-9]|[1-9]|1[0-2])\2\d{4}'
    DATE_REGEX_PTBR2: Final[str] = r'^(?:(?:31([-\/.]?)(?:0[13578]|1[02]))\1|(?:(?:29|30)([-\/.]?)(?:0[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)\d{2})$|^(?:29([-\/.]?)02\3(?:(?:(?:1[6-9]|[2-9]\d)(?:0[48]|[2468][048]|[13579][26]))))$|^(?:0[1-9]|1\d|2[0-8])([-\/.]?)(?:(?:0[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)\d{2})$'
    DATE_REGEX_PTBR3: Final[str] = r'[\s]?([0-9]|[0-9][0-9]) ((de|em)) '
    DATE_REGEX_PTBR4: Final[str] = r'[-\/.](\d{4}|\d{2})'


    def process_dates_en(self, transient_tweet_text):
        '''
        Identify date and convert it to constant
        '''
        transient_tweet_text = re.sub(self.DATE_REGEX_EN1, self.CONSTANT_DATE, transient_tweet_text)
        transient_tweet_text = re.sub(self.DATE_REGEX_EN2, self.CONSTANT_DATE, transient_tweet_text)

        Months = self.regex_or('january','jan','february','feb','march','mar','april','may','june','jun','july','jul','august','aug','september','sep','october','oct','november','nov','december','dec')

        date_regex3 = self.DATE_REGEX_EN3 + Months
        transient_tweet_text = re.sub(date_regex3, self.CONSTANT_DATE, transient_tweet_text)
        
        date_regex4 = Months + self.DATE_REGEX_EN4
        transient_tweet_text = re.sub(date_regex4, self.CONSTANT_DATE, transient_tweet_text)

        transient_tweet_text = re.sub(self.DATE_REGEX_EN5, self.CONSTANT_DATE, transient_tweet_text)
        transient_tweet_text = re.sub(self.DATE_REGEX_EN6, self.CONSTANT_DATE, transient_tweet_text)

        return transient_tweet_text

    def process_dates_ptbr(self, transient_tweet_text):
        '''
        Identify date and convert it to constant
        '''
        transient_tweet_text = re.sub(self.DATE_REGEX_PTBR1, self.CONSTANT_DATE, transient_tweet_text)
        transient_tweet_text = re.sub(self.DATE_REGEX_PTBR2, self.CONSTANT_DATE, transient_tweet_text)

        Months = self.regex_or('janeiro', 'jan', 'fevereiro', 'fev', 'março', 'mar', 'abril', 'abr', 'maio', 'maio', 'junho', 'jun', 'julho', 'jul', 'agosto', 'ago', 'setembro', 'set', 'outubro', 'out', 'novembro', 'nov', 'dezembro', 'dez')

        date_regex3 = self.DATE_REGEX_PTBR3 + Months
        transient_tweet_text = re.sub(date_regex3, self.CONSTANT_DATE, transient_tweet_text)

        date_regex4 = Months + self.DATE_REGEX_PTBR4
        transient_tweet_text = re.sub(date_regex4, self.CONSTANT_DATE, transient_tweet_text)

        return transient_tweet_text

    def process_times(self, transient_tweet_text):
        '''
        Indentify time and convert it to constant
        '''
        return re.sub(self.TIME_REGEX, self.CONSTANT_TIME, transient_tweet_text)

    def tratar_texto(self, texto):
        texto = self.strip_unicode(texto)
        texto = self.to_lowercase(texto)
        texto = self.process_times(texto)
        texto = self.process_dates_en(texto)
        texto = self.process_dates_ptbr(texto)
        return texto


def test_print():
    test_tweet = """ Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)
    Brasília, 9 de março
    Com participação de argentinos, PARLASUL volta a se reunir em 2 de julho.
    De acordo com a Constituição, o Congresso Nacional se reúne de 1 de fevereiro a 17 de julho e de 1 de agosto a 22 de dezembro.
    Em infográficos, tabelas, créditos de imagens ou textos de legenda, pode-se usar a data de forma abreviada. Nesse caso, separe os números por barra e use zero antes dos números: 07/02/2012."""
    tratamento = TratamentoDataEHora()

    #General Proprocessing
    test_tweet = test_tweet.lower()

    #function tests
    print("Remove Dates:\n", tratamento.process_dates_en(test_tweet))
    print("Process Time:\n", tratamento.process_times(test_tweet))

def test_trata_texto():
    test_tweet = """ Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)
    Brasília, 9 de março
    Com participação de argentinos, PARLASUL volta a se reunir em 2 de julho.
    De acordo com a Constituição, o Congresso Nacional se reúne de 1 de fevereiro a 17 de julho e de 1 de agosto a 22 de dezembro.
    Em infográficos, tabelas, créditos de imagens ou textos de legenda, pode-se usar a data de forma abreviada. Nesse caso, separe os números por barra e use zero antes dos números: 07/02/2012.
    rt  constantenaomencaodamarca : meu pl a suspensao das metas ate jun/22. bolsonaro argumenta que deu fim a emergencia em saude publica de importancia nacio...
    rt  constantenaomencaodamarca : meu pl a suspensao das metas ate dez/2050. bolsonaro argumenta que deu fim a emergencia em saude publica de importancia nacio...
    """
    tratamento = TratamentoDataEHora()
    test_tweet = test_tweet.lower()
    tweet_tratado = tratamento.tratar_texto(test_tweet)
    print('tweet:', test_tweet)
    print('tweet_tratado:', tweet_tratado)

def main():
    test_print()
    test_trata_texto()

if __name__ == '__main__':
    main()
