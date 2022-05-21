import glob
import json
import uuid

class SearchKeys:

    def __init__(self, lang):
        self.lang = lang
        self.twitter_logic_and_query = 'AND'

    def read_json(self, file_path):
        content = None
        with open(file_path) as f:
            content = json.load(f)
        return content

    def __build_query_list(self, first_pos_list, second_pos_list, func_build_string):
        query_list = []
        for first_pos in first_pos_list:
            for second_pos in second_pos_list:
                query_dict_line =  func_build_string(first_pos, second_pos)
                query_list.append(query_dict_line)
        return query_list
    
    def __build_separeted_query_list(self, first_pos_list, second_pos_list):
        query_list = []
        for first_pos in first_pos_list:
            query_list.append({'q': f'{first_pos}'})
        for second_pos in second_pos_list:
            query_list.append({'q': f'{second_pos}'})
        return query_list

    def __build_string_twitter_lang(self, first_pos, second_pos):
        return {'q': f'{first_pos} {self.twitter_logic_and_query} {second_pos}', 'lang': self.lang}

    def get_twitter_query_covid_lang(self, first_pos_list, second_pos_list):
        return self.__build_query_list(first_pos_list, second_pos_list, self.__build_string_twitter_lang)

    def __build_string_youtube_search_list(self, first_pos, second_pos):
        return {'q': f'{first_pos} {second_pos}'}

    def get_youtube_search_list_query_covid(self, first_pos_list, second_pos_list):
        return self.__build_query_list(first_pos_list, second_pos_list, self.__build_string_youtube_search_list)

    def get_youtube_search_list_separeted_query_covid(self, first_pos_list, second_pos_list):
        return self.__build_separeted_query_list(first_pos_list, second_pos_list)

    def __build_string_idvideo_youtube(self, first_pos):
        return {'q': f'{first_pos}'}

    def get_youtube_idvideo_from_search_list_file(self, path, extension):
        path_to_matching = f'{path}*{extension}'
        file_list = glob.glob(path_to_matching)
        query_list = []
        for file in file_list:
            data = self.read_json(file)
            for content in data:
                videoId = str(uuid.uuid4())
                if 'videoId' in content['id']:
                    videoId = content['id']['videoId']
                query_dict_line = self.__build_string_idvideo_youtube(videoId)
                query_list.append(query_dict_line)
        return query_list

    def __build_string_youtube_separeted_terms_list(self, first_pos, second_pos):
        return {'first_term': f'{first_pos} ', 'second_term': f'{second_pos}'}

    def get_youtube_separeted_terms_seach_list_query_covid(self, first_pos_list, second_pos_list):
        return self.__build_query_list(first_pos_list, second_pos_list, self.__build_string_youtube_separeted_terms_list)