import glob
import json
from SearchBase import SearchBase
from SearchKeys import SearchKeys

class FilterYouTubeCommentThreads:

    def read_json(self, file_path):
        content = None
        with open(file_path) as f:
            content = json.load(f)
        return content
    
    def verify_text_match_search(self, text, terms_match):
        new_text = text.lower().strip()
        for term in terms_match:
            first_term = term['first_term'].lower().strip()
            second_term = term['second_term'].lower().strip()
            if first_term in new_text and second_term in new_text:
                return True
        return False

    def get_youtube_idvideo_from_search_list_file(self, path, extension, search_match, func_save_json):
        path_to_matching = f'{path}*{extension}'
        file_list = glob.glob(path_to_matching)
        for file in file_list:
            data = self.read_json(file)
            for content in data:
                text_original = content['snippet']['topLevelComment']['snippet']['textOriginal']
                is_match = self.verify_text_match_search(text_original, search_match)
                if is_match:
                    id = content['id']
                    file_name = f'data/raw/youtube/filtered_comment_threads/{id}.json'
                    func_save_json(file_name, content)


def main():
    filter = FilterYouTubeCommentThreads()
    path = 'data/raw/youtube/comment_threads/'
    extension = '.json'

    search = SearchBase()
    
    func_get_query_to_search = SearchKeys('pt').get_youtube_separeted_terms_seach_list_query_covid
    func_save_json = search.save_json

    search_match = search.load_search_query_list_dict(func_get_query_to_search)
    pesquisa = filter.get_youtube_idvideo_from_search_list_file(path, extension, search_match, func_save_json)

if __name__ == '__main__':
    main()
