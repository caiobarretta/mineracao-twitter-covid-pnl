from typing import Final

class TratamentoTextoBase:
    BLANK_SPACE: Final[str] = ' '
    def regex_or(self, *items):
        r = '|'.join(items)
        r = '(' + r + ')'
        return r
    def strip_unicode(self, transient_tweet_text):
        '''
        Strip all unicode characters from a tweet
        '''
        tweet = ''.join(i for i in transient_tweet_text if ord(i)<128)
        return tweet 