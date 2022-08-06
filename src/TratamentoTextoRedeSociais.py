import re
from typing import Final
from TratamentoTextoBase import TratamentoTextoBase

class TratamentoTextoRedeSociais(TratamentoTextoBase):
    PROCESS_MENTIONS_REGEX: Final[str] = r"@(\w+)"
    CONSTANT_NON_BRAND_MENTION: Final[str] = " constantenaomencaodamarca "

    PROCESS_HASHTAGS_REGEX: Final[str] = r"#(\w+)\b"
    CONSTANT_HASHTAG: Final[str] = " hashtagconstante "

    def tratar_texto(self, texto):
        texto = self.strip_unicode(texto)
        texto = self.to_lowercase(texto)
        texto = self.process_hashtags(texto)
        texto = self.process_mentions(texto)
        return texto

    def process_mentions(self, transient_tweet_text):
        '''
        Identify mentions if any
        '''
        return re.sub(self.PROCESS_MENTIONS_REGEX, self.CONSTANT_NON_BRAND_MENTION, transient_tweet_text)

    def process_hashtags(self, transient_tweet_text):
        '''
        Strip all Hashtags from a tweet
        '''
        return re.sub(self.PROCESS_HASHTAGS_REGEX, self.CONSTANT_HASHTAG, transient_tweet_text)


def test_trata_texto():
    test_tweet = "Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)"
    tratamento = TratamentoTextoRedeSociais()
    
    #General Proprocessing
    test_tweet = test_tweet.lower()
        
    #function tests
    print("Remove mentions:\n", tratamento.process_mentions(test_tweet))
    print("Remove Hashtags:\n",tratamento.process_hashtags(test_tweet))

def main():
    test_trata_texto()

if __name__ == '__main__':
    main()