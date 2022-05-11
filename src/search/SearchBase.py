import json
import time
from os.path import exists

class SearchBase:

    def save_json(self, file_name, content, replace_existing_file = True):
        file_exists = False
        if not replace_existing_file:
            file_exists = exists(file_name)
        if not file_exists:
            with open(file_name, "w") as f:
                json.dump(content, f, indent=2)

    def get_lists_of_keys_to_search(self):
        hashtag_SUS_list = ['#SUS', '#SistemaUnicoDeSaude', '#SistemaUnicoSaude', '#SaúdePública', '#SaudePublica', '#SistemaDeSaudePublico',  '#SistemaSaudePublico', '#SistemaDeSaúdePúblico',  '#SistemaSaúdePúblico']
        SUS_list = ['SUS', 'S.U.S', 'Sistema único de saúde', 'Sistema unico de saude', 'Saúde Pública', 'Saude Publica', 'Sistema De Saude Publico', 'Sistema Saude Publico', 'Sistema De Saúde Público',  'Sistema Saúde Público']
        hashtag_COVID_list = ['#COVID', '#COIVD', '#COIVD-19', '#COVID-19', '#CORONA', '#CORONAVIRUS', '#SARS','#SARSCoV2','#SARS-CoV-2', '#CoV', '#Pandemia', '#PandemiaCovid', '#PandemiaCorona', '#PandemiaCoronavirus']
        COVID_list = ['COVID', 'COIVD', 'COVID-19', 'COIVD-19','CORONA', 'CORONAVÍRUS', 'CORONAVIRUS', 'CORONA VIRUS', 'SARS','SARSCoV2','SARS-CoV-2', 'CoV', 'Pandemia', 'Pandemia Covid', 'Pandemia Corona', 'Pandemia Corona vírus']
        return hashtag_SUS_list, SUS_list, hashtag_COVID_list, COVID_list

    def load_dict_to_search(self, func_get_query_to_search, first_list, second_list, list_of_dict_to_fill):
        lst_dict = func_get_query_to_search(first_list, second_list)
        for dict in lst_dict:
            list_of_dict_to_fill.append(dict)

    def load_search_query_list_dict(self, func_get_query_to_search):
        pesquisa = []
        hashtag_SUS_list, SUS_list, hashtag_COVID_list, COVID_list = self.get_lists_of_keys_to_search()
        
        #hashtag_SUS_list and hashtag_COVID_list
        self.load_dict_to_search(func_get_query_to_search, hashtag_SUS_list, hashtag_COVID_list, pesquisa)
        #hashtag_SUS_list and COVID_list
        self.load_dict_to_search(func_get_query_to_search, hashtag_SUS_list, COVID_list, pesquisa)
        #SUS_list and hashtag_COVID_list
        self.load_dict_to_search(func_get_query_to_search, SUS_list, hashtag_COVID_list, pesquisa)
        #SUS_list and COVID_list
        self.load_dict_to_search(func_get_query_to_search, SUS_list, COVID_list, pesquisa)

        return pesquisa

    def load_search(self, file_credentials, pesquisa, func_get_new_instance_api, func_get_and_save_data):
        api = func_get_new_instance_api(file_credentials)
        quantidade_maxima_de_tentativas = 10
        query_counter = 0

        print(f'Inicializando pesquisa na API {api.get_api_name()}')
        print(f'Quantidades de itens da pesquisa: {len(pesquisa)}')
        for pesquisa in pesquisa:
            query = pesquisa['q']
            lang = ''
            if 'lang' in pesquisa:
                lang = pesquisa['lang']
            tentativas = 0
            continuar = True
            error = False
            while continuar:
                try:
                    print(f'Pesquisa: {query}|{lang} query_counter: {query_counter}')
                    func_get_and_save_data(api, query, lang)
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
                        api = func_get_new_instance_api(file_credentials)
                        if tentativas > quantidade_maxima_de_tentativas:
                            continuar = False
                    else:
                        continuar = False
