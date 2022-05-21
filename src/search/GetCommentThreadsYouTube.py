import time
from SearchBase import SearchBase
from api.YouTubeAPI import YouTubeAPI
from SearchKeys import SearchKeys
from os.path import exists

class SearchListYouTube(SearchBase):
    def __init__(self, replace_existing_tweets = True, verify_comments_loaded = True, yt_time_sleep_load_search = 0):
        self.replace_existing_tweets = replace_existing_tweets
        self.verify_comments_loaded = verify_comments_loaded
        self.path_comments_loaded = 'data/raw/youtube/comments_loaded.json'
        super().__init__(yt_time_sleep_load_search)

    def save_search_list(self, search_list):
        for video in search_list:
            video_id = video['id']
            print(f'salvando video pesquisa: {video_id} para arquivo.')
            file_name = f'data/raw/youtube/comment_threads/{video_id}.json'
            content = search_list
            self.save_json(file_name, content, self.replace_existing_tweets)
            time.sleep(1)

    def get_and_save_search_list(self, api, query, lang):
        loaded = False
        if self.verify_comments_loaded:
            data_comments_loaded = self.get_file_comments_loaded()
            if data_comments_loaded and len(data_comments_loaded):
                loaded = self.is_comment_loaded(data_comments_loaded, query)
            else:
                self.create_file_comments_loaded()
        if not loaded:
            print(f'carregando os resultados da pesquisa: {query} na api do YT')
            search_list = api.load_comments_from_videoid_with_threads(query)
            print(f'quantidade de resultados da pesquisa: {query}|{lang} carregados com sucesso.')
            self.save_search_list(search_list)
            if self.verify_comments_loaded:
                self.append_data_file_comments_loaded({'id': query})
        else:
            print(f'comentários para o vídeId: {query} já carregados.')
                

    def get_new_instance_api(self, file_credentials):
        return YouTubeAPI(file_credentials)


    def get_file_comments_loaded(self):
        if exists(self.path_comments_loaded):
            return self.read_json(self.path_comments_loaded)
        else:
            return None

    def append_data_file_comments_loaded(self, data):
        data_comments_loaded = self.get_file_comments_loaded()
        if data_comments_loaded and len(data_comments_loaded):
            data_comments_loaded.append(data)
            self.save_json(self.path_comments_loaded, data_comments_loaded)
        else:
            self.create_file_comments_loaded()
            self.save_json(self.path_comments_loaded, [data])

    def create_file_comments_loaded(self):
        if not exists(self.path_comments_loaded):
            self.save_json(self.path_comments_loaded, [])

    def is_comment_loaded(self, data, id):
        for line in data:
            if line['id'] == id:
                return True
        return False
    
def main():
    search = SearchListYouTube(False)
    file_credentials = 'src/search/credentials.yaml'

    search_keys = SearchKeys('pt')

    func_get_new_instance_api = search.get_new_instance_api
    func_get_and_save_data = search.get_and_save_search_list

    path = 'data/raw/youtube/search_list/'
    extension = '.json'
    pesquisa = search_keys.get_youtube_idvideo_from_search_list_file(path, extension)

    search.load_search(file_credentials, pesquisa, func_get_new_instance_api, func_get_and_save_data)

if __name__ == '__main__':
    main()
