import json
import time
from tweepy.errors import TooManyRequests
from TweepyAPI import TweepyAPI


def save_json(file_name, content):
    with open(file_name, "w") as f:
        json.dump(content, f, indent=2)

def save_tweets(tweets):
    try:
        for tweet in tweets:
            print(f'salvando tweet: {tweet.id} para arquivo.')
            file_name = f'data/raw/twitter/{tweet.id}.json'
            content = tweet._json
            save_json(file_name, content)
            time.sleep(1)
    except TooManyRequests:
            print(f'Ocorreu um erro: {TooManyRequests}')

def get_and_save_tweets(api, query, lang):
    print(f'carregando os tweets da pesquisa: {query}|{lang}')
    tweets = api.search_tweets(query, lang)
    print(f'tweets da pesquisa: {query}|{lang} carregados com sucesso.')
    save_tweets(tweets)


file_credentials = 'src/credentials.yaml'
api = TweepyAPI(file_credentials)

pesquisas = [
        {'q':'#SUS AND #COVID', 'lang':'pt'},
        {'q':'#SUS AND #COVID-19', 'lang':'pt'},
        {'q':'#SUS AND #CORONA', 'lang':'pt'},
        {'q':'#SUS AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'SUS AND #COVID', 'lang':'pt'},
        {'q':'SUS AND #COVID-19', 'lang':'pt'},
        {'q':'SUS AND #CORONA', 'lang':'pt'},
        {'q':'SUS AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'#SUS AND COVID', 'lang':'pt'},
        {'q':'#SUS AND COVID-19', 'lang':'pt'},
        {'q':'#SUS AND CORONA', 'lang':'pt'},
        {'q':'#SUS AND CORONAVIRUS', 'lang':'pt'},
        {'q':'#SUS AND CORONA VIRUS', 'lang':'pt'},

        {'q':'S.U.S AND COVID', 'lang':'pt'},
        {'q':'S.U.S AND COVID-19', 'lang':'pt'},
        {'q':'S.U.S AND CORONA', 'lang':'pt'},
        {'q':'S.U.S AND CORONAVIRUS', 'lang':'pt'},
        {'q':'S.U.S AND CORONA VIRUS', 'lang':'pt'},

        {'q':'S.U.S AND #COVID', 'lang':'pt'},
        {'q':'S.U.S AND #COVID-19', 'lang':'pt'},
        {'q':'S.U.S AND #CORONA', 'lang':'pt'},
        {'q':'S.U.S AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'SUS AND COVID', 'lang':'pt'},
        {'q':'SUS AND COVID-19', 'lang':'pt'},
        {'q':'SUS AND CORONA', 'lang':'pt'},
        {'q':'SUS AND CORONAVIRUS', 'lang':'pt'},
        {'q':'SUS AND CORONA VIRUS', 'lang':'pt'},

        {'q':'Sistema único de saúde AND COVID', 'lang':'pt'},
        {'q':'Sistema único de saúde AND COVID-19', 'lang':'pt'},
        {'q':'Sistema único de saúde AND CORONA', 'lang':'pt'},
        {'q':'Sistema único de saúde AND CORONAVIRUS', 'lang':'pt'},
        {'q':'Sistema único de saúde AND CORONA VIRUS', 'lang':'pt'},

        {'q':'Sistema único de saúde AND #COVID', 'lang':'pt'},
        {'q':'Sistema único de saúde AND #COVID-19', 'lang':'pt'},
        {'q':'Sistema único de saúde AND #CORONA', 'lang':'pt'},
        {'q':'Sistema único de saúde AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'Sistema unico de saude AND #COVID', 'lang':'pt'},
        {'q':'Sistema unico de saude AND #COVID-19', 'lang':'pt'},
        {'q':'Sistema unico de saude AND #CORONA', 'lang':'pt'},
        {'q':'Sistema unico de saude AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'#SistemaUnicoDeSaude AND #COVID', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND #COVID-19', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND #CORONA', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'#SistemaUnicoSaude AND #COVID', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND #COVID-19', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND #CORONA', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND #CORONAVIRUS', 'lang':'pt'},

        {'q':'#SistemaUnicoDeSaude AND COVID', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND COVID-19', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND CORONA', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND CORONAVIRUS', 'lang':'pt'},
        {'q':'#SistemaUnicoDeSaude AND CORONA VIRUS', 'lang':'pt'},

        {'q':'#SistemaUnicoSaude AND COVID', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND COVID-19', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND CORONA', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND CORONAVIRUS', 'lang':'pt'},
        {'q':'#SistemaUnicoSaude AND CORONA VIRUS', 'lang':'pt'},
    ]

quantidade_maxima_de_tentativas = 10
query_counter = 0

print(f'Inicializando pesquisa no twitter')
print(f'Quantidades de itens da pesquisa: {len(pesquisas)}')
for pesquisa in pesquisas:
    query = pesquisa['q']
    lang = pesquisa['lang']
    tentativas = 0
    continuar = True
    error = False
    while continuar:
        try:
            print(f'Pesquisa: {query}|{lang} query_counter: {query_counter}')
            get_and_save_tweets(api, query, lang)
            query_counter = query_counter + 1
            time.sleep(20)
        except NameError:
            print(f'Ocorreu um erro: {NameError} na query: {query} lang: {lang} query_counter: {query_counter}')
            tentativas = tentativas + 1
            error = True
        finally:
            if error:
                print(f'Retomando pesquisa na query: {query} lang: {lang} query_counter: {query_counter}')
                time.sleep(20)
                api = TweepyAPI(file_credentials)
                if tentativas > quantidade_maxima_de_tentativas:
                    continuar = False
            else:
                continuar = False
