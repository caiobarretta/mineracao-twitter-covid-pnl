import time
from SearchBase import SearchBase
from SearchKeys import SearchKeys
from api.YouTubeAPI import YouTubeAPI


class SearchListYouTube(SearchBase):
    def __init__(self, quantidade_maxima_resultados = 10) -> None:
        super().__init__()
        self.quantidade_maxima_resultados = quantidade_maxima_resultados
    
    def save_search_list(self, search_list):
        for video in search_list:
            videoId = video['id']['videoId']
            print(f'salvando video pesquisa: {videoId} para arquivo.')
            file_name = f'data/raw/youtube/search_list/{videoId}.json'
            content = search_list
            self.save_json(file_name, content)
            time.sleep(1)

    def get_and_save_search_list(self, api, query, lang):
        print(f'carregando os resultados da pesquisa: {query} na api do YT')
        search_list = api.search_list(query, self.quantidade_maxima_resultados)
        print(f'quantidade de resultados da pesquisa: {query}|{lang} carregados com sucesso.')
        self.save_search_list(search_list)
    
    def get_new_instance_api(self, file_credentials):
        return YouTubeAPI(file_credentials)
    

def main():
    search = SearchListYouTube()
    file_credentials = 'src/credentials.yaml'

    func_get_new_instance_api = search.get_new_instance_api
    func_get_query_to_search = SearchKeys('pt').get_youtube_search_list_query_covid
    func_get_and_save_data = search.get_and_save_search_list

    pesquisa = search.load_search_query_list_dict(func_get_query_to_search)

    search.load_search(file_credentials, pesquisa, func_get_new_instance_api, func_get_and_save_data)

if __name__ == '__main__':
    main()
