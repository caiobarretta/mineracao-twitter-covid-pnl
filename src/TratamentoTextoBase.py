from typing import Final

class TratamentoTextoBase:
    BLANK_SPACE: Final[str] = ' '
    def regex_or(self, *items):
        r = '|'.join(items)
        r = '(' + r + ')'
        return r