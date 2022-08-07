import re
from typing import Final
from TratamentoTextoBase import TratamentoTextoBase

class TratamentoNumerico(TratamentoTextoBase):
    CONSTANT_NUM_WITHOUT_BLANK_SPACE: Final[str] = "constante_numerica" 
    CONSTANT_ALPHA_NUM_WITHOUT_BLANK_SPACE: Final[str] = "constante_alfanumerica"

    CONSTANT_NUM: Final[str] = f" {CONSTANT_NUM_WITHOUT_BLANK_SPACE} "
    CONSTANT_MONEY: Final[str] = " constante_dinheiro "
    CONSTANT_ALPHA_NUM: Final[str] = f" {CONSTANT_ALPHA_NUM_WITHOUT_BLANK_SPACE} "

    MONEY_REGEX1: Final[str] = r'\b(r$|rs|\$)[\s]*('+CONSTANT_NUM_WITHOUT_BLANK_SPACE+')?[\.]?[\s]*'+CONSTANT_NUM_WITHOUT_BLANK_SPACE+'\b'
    MONEY_REGEX2: Final[str] = r'[\s]*[\.]?[\s]*'+CONSTANT_NUM_WITHOUT_BLANK_SPACE+'(cent[s]?|\$|c|reais)\b'
    MONEY_REGEX3: Final[str] = r'(\$|rs|r$)[\s]*'+CONSTANT_ALPHA_NUM_WITHOUT_BLANK_SPACE

    NUM_REGEX = r'(?<!#)\b(?:[-+]?[\d,]*[\.]?[\d,]*[\d]+|\d+)\b'
    ALPHA_NUMERIC_REGEX: Final[str] = r'(?<!#)\b(?:([a-z]+[0-9]+[a-z]*|[a-z]*[0-9]+[a-z]+)[a-z,0-9]*)\b'

    def indentify_money(self, transient_tweet_text):
        '''
        identify money in the tweet text but outside offers. This includes $,Rs, pound, Euro
        '''
        transient_tweet_text = re.sub(self.MONEY_REGEX1, self.CONSTANT_MONEY, transient_tweet_text)
        transient_tweet_text = re.sub(self.MONEY_REGEX2, self.CONSTANT_MONEY, transient_tweet_text)
        transient_tweet_text = re.sub(self.MONEY_REGEX3, self.CONSTANT_MONEY, transient_tweet_text)
        return transient_tweet_text

    def replace_numbers(self, transient_tweet_text):
        '''
        Given any number/interger in tweet text, we want it to be replaced by constantnum
        '''
        # we want to process only those numbers that are not in a hashtag - below logic does this
        transient_tweet_text = re.sub(self.NUM_REGEX, self.CONSTANT_NUM , transient_tweet_text)
        return transient_tweet_text

    def identify_alpha_numerics(self, transient_tweet_text):
        '''
        Identify alpha numerics - this helps in identifying product codes/models, promocodes, Order IDs
        '''
        
        transient_tweet_text = re.sub(self.ALPHA_NUMERIC_REGEX, self.CONSTANT_ALPHA_NUM, transient_tweet_text)
        return transient_tweet_text

    def tratar_texto(self, texto):
        texto = self.strip_unicode(texto)
        texto = self.to_lowercase(texto)
        texto = self.identify_alpha_numerics(texto)
        texto = self.replace_numbers(texto)
        texto = self.indentify_money(texto)
        return texto

def test_trata_texto():
    test_tweet = """ 
        Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)
        R$ 20,00, R$ 30.00, R$ 4.000
        "rt @jairbolsonaro: - o @minsaude converte 6,4 mil leitos de unidade de terapia intensiva (uti) exclusivos para covid em leitos convencionai...",
        "rt  constantenaomencaodamarca : certas coisas nao tem preco... mas c bolsocard vc pode gastar 12,53 mi/mes e depois esconder debaixo d tapete ! agora os 790mi...",
    """
    tratamento = TratamentoNumerico()
    test_tweet = test_tweet.lower()
    tweet_tratado = tratamento.tratar_texto(test_tweet)
    print('tweet:', test_tweet)
    print('tweet_tratado:', tweet_tratado)

def main():
    test_trata_texto()

if __name__ == '__main__':
    main()