import glob
import json
from search.SearchBase import SearchBase

from search.SearchKeys import SearchKeys

class FilterYouTubeCommentThreads:

    def read_json(self, file_path):
        content = None
        with open(file_path) as f:
            content = json.load(f)
        return content
    
    def get_youtube_idvideo_from_search_list_file(self, path, extension):
        path_to_matching = f'{path}*{extension}'
        file_list = glob.glob(path_to_matching)
        query_list = []
        for file in file_list[0:1]:
            data = self.read_json(file)
            for content in data[0:1]:
                text_original = content['snippet']['topLevelComment']['snippet']['textOriginal']
                print(text_original)
        #    #    query_dict_line = self.__build_string_idvideo_youtube(videoId)
        #    #    query_list.append(query_dict_line)
        return query_list


def main():
    filter = FilterYouTubeCommentThreads()
    path = 'data/raw/youtube/comment_threads/'
    extension = '.json'

    search = SearchBase()
    
    func_get_query_to_search = SearchKeys('pt').get_youtube_search_list_query_covid
    pesquisa = search.load_search_query_list_dict(func_get_query_to_search)
    print(pesquisa)
    #pesquisa = filter.get_youtube_idvideo_from_search_list_file(path, extension)

if __name__ == '__main__':
    main()
