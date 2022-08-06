import re
import string

class TrataTextoRedeSociais:
    def tratar_texto(self, texto):
        transient_tweet_text = texto
        transient_tweet_text = self.process_hashtags(transient_tweet_text)
        transient_tweet_text = self.process_mentions(transient_tweet_text)

    def process_mentions(transient_tweet_text):
        '''
        Identify mentions if any
        '''
        transient_tweet_text = re.sub(r"@(\w+)", " constantenaomencaodamarca ", transient_tweet_text)
        return transient_tweet_text

    def process_hashtags(transient_tweet_text):
        '''
        Strip all Hashtags from a tweet
        '''
        transient_tweet_text = re.sub(r"#(\w+)\b", ' hashtagconstante ', transient_tweet_text)
        return transient_tweet_text


def test_trata_texto():
    test_tweet = "Nice @varun paytm @paytm saver abc@gmail.com sizes for the wolf on 20/10/2010 at 10:00PM  grey/deep royal-volt Nike Air Skylon II retro are 40% OFF for a limited time at $59.99 + FREE shipping.BUY HERE -> https://bit.ly/2L2n7rB (promotion - use code MEMDAYSV at checkout)"
    tratamento = TrataTextoRedeSociais()
    
    #General Proprocessing
    test_tweet = test_tweet.lower()
    test_tweet = tratamento.strip_unicode(test_tweet)
    
    #function tests
    print("Remove mentions:\n", tratamento.process_mentions(test_tweet))
    print("Remove Hashtags:\n",tratamento.process_hashtags(test_tweet))

def main():
    test_trata_texto()

if __name__ == '__main__':
    main()