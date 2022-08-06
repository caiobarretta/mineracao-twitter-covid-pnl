import re
from typing import Final
from TratamentoTextoBase import TratamentoTextoBase

class TratamentoBasicoTexto(TratamentoTextoBase):
    SPL_WORD_E: Final[str] = '&amp;'
    WORD_E: Final[str] = ' e '
    
    STRIP_WHITESPACES_REGEX: Final[str] = r'[\s]+'

    EMAIL_REGEX: Final[str] = r'(\b)?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\b)?'
    CONSTANT_EMAIL_ID: Final[str] = ' constanteemailid '

    def trim(self, transient_tweet_text):
        ''' 
        trim leading and trailing spaces in the tweet text
        '''
        return transient_tweet_text.strip()

    def strip_whitespaces_regex(self, transient_tweet_text):
        '''
        Strip all white spaces
        '''
        transient_tweet_text = re.sub(self.STRIP_WHITESPACES_REGEX, self.BLANK_SPACE, transient_tweet_text)
        return transient_tweet_text

    def to_lowercase(self, transient_tweet_text):
        '''
        Convert tweet text to lower to lower case alphabets
        '''
        transient_tweet_text = transient_tweet_text.lower()
        return transient_tweet_text

    def remove_spl_words(self, transient_tweet_text):
        return transient_tweet_text.replace(self.SPL_WORD_E, self.WORD_E)

    def strip_unicode(self, transient_tweet_text):
        '''
        Strip all unicode characters from a tweet
        '''
        tweet = ''.join(i for i in transient_tweet_text if ord(i)<128)
        return tweet

    def process_email_ids(self, transient_tweet_text):
        '''
        identify email mentioned if any
        '''
        transient_tweet_text = re.sub(self.EMAIL_REGEX, self.CONSTANT_EMAIL_ID, transient_tweet_text)
        return transient_tweet_text

    def strip_whitespaces_regex(self, transient_tweet_text):
        '''
        Strip all white spaces
        '''
        transient_tweet_text = re.sub(r'[\s]+', ' ', transient_tweet_text)
        return transient_tweet_text

    def tratar_texto(self, texto):
        texto = self.strip_unicode(texto)
        texto = self.to_lowercase(texto)
        texto = self.trim(texto)
        texto = self.strip_whitespaces_regex(texto)
        texto = self.remove_spl_words(texto)

        texto = self.process_email_ids(texto)
        texto = self.strip_unicode(texto)

        texto = self.trim(texto)
        texto = self.strip_whitespaces_regex(texto)

        return texto

 
def test_print():
    test_tweet = "Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)"
    tratamento = TratamentoBasicoTexto()

    #General Proprocessing
    test_tweet = test_tweet.lower()
    test_tweet = tratamento.strip_unicode(test_tweet)

    #function tests
    print('Remove Emailid:\n', tratamento.process_email_ids(test_tweet))

def test_trata_texto():
    test_tweet = " Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)"
    tratamento = TratamentoBasicoTexto()
    test_tweet = test_tweet.lower()
    tweet_tratado = tratamento.tratar_texto(test_tweet)
    print('tweet:', test_tweet)
    print('tweet_tratado:', tweet_tratado)

def main():
    test_print()
    test_trata_texto()

if __name__ == '__main__':
    main()