import time
from SearchBase import SearchBase
from api.YouTubeAPI import YouTubeAPI
from SearchKeys import SearchKeys


class SearchListYouTube(SearchBase):
    def __init__(self) -> None:
        super().__init__()

    def save_search_list(self, search_list):
        for video in search_list:
            videoId = video['id']
            print(f'salvando video pesquisa: {videoId} para arquivo.')
            file_name = f'data/raw/youtube/comment_threads/{videoId}.json'
            content = search_list
            self.save_json(file_name, content, False)
            time.sleep(1)

    def get_and_save_search_list(self, api, query, lang):
        print(f'carregando os resultados da pesquisa: {query} na api do YT')
        search_list = api.load_comments_from_videoid_with_threads(query)
        print(f'quantidade de resultados da pesquisa: {query}|{lang} carregados com sucesso.')
        self.save_search_list(search_list)

    def get_new_instance_api(self, file_credentials):
        return YouTubeAPI(file_credentials)
    
def main():
    search = SearchListYouTube()
    file_credentials = 'src/credentials.yaml'

    search_keys = SearchKeys('pt')

    func_get_new_instance_api = search.get_new_instance_api
    func_get_and_save_data = search.get_and_save_search_list

    path = 'data/raw/youtube/search_list/'
    extension = '.json'
    pesquisa = search_keys.get_youtube_idvideo_from_search_list_file(path, extension)

    search.load_search(file_credentials, pesquisa, func_get_new_instance_api, func_get_and_save_data)

if __name__ == '__main__':
    main()
