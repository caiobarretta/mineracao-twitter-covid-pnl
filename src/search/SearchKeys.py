
class SearchKeys:

    def __init__(self, lang):
        self.lang = lang
        self.twitter_logic_and_query = 'AND'

    def __build_query_list(self, first_pos_list, second_pos_list, func_build_string):
        query_list = []
        for first_pos in first_pos_list:
            for second_pos in second_pos_list:
                query_dict_line =  func_build_string(first_pos, second_pos)
                query_list.append(query_dict_line)
        return query_list 

    def __build_string_twitter_lang(self, first_pos, second_pos):
        return {'q': f'{first_pos} {self.twitter_logic_and_query} {second_pos}', 'lang': self.lang}

    def get_twitter_query_covid_lang(self, first_pos_list, second_pos_list):
        return self.__build_query_list(first_pos_list, second_pos_list, self.__build_string_twitter_lang)

    def __build_string_youtube_search_list(self, first_pos, second_pos):
        return {'q': f'{first_pos} {second_pos}'}

    def get_youtube_search_list_query_covid(self, first_pos_list, second_pos_list):
        return self.__build_query_list(first_pos_list, second_pos_list, self.__build_string_youtube_search_list)