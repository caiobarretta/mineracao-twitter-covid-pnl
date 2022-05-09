from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

import yaml
from yaml.loader import SafeLoader

class YouTubeAPI:
    def __init__(self, file_name_credentials):
        self.file_name_credentials = file_name_credentials
    
    def get_credentials(self):
        with open(self.file_name_credentials) as f:
            data = yaml.load(f, Loader=SafeLoader)
        return data['youtube_api_service_name'],data['youtube_api_version'],data['developer_key']

    def get_comments(self, youtube, parent_id):
        results = youtube.comments().list(part='id,snippet',
                                        parentId=parent_id,
                                        textFormat='plainText').execute()
        return results['items']

    def get_comment_threads(self, youtube, video_id):
        threads = []
        try:
            results = youtube.commentThreads().list(part='id,snippet',
                                                    videoId=video_id,
                                                    textFormat='plainText',
                                                    order='relevance').execute()
            for item in results['items']:
                threads.append(item)

            while 'nextPageToken' in results:
                pageToken = results['nextPageToken']
                results = youtube.commentThreads().list(part='snippet',
                                                        videoId=video_id,
                                                        pageToken=pageToken,
                                                        textFormat='plainText',
                                                        order='relevance').execute()
            for item in results['items']:
                threads.append(item)
        except HttpError as error:
            print(f'ocorreu um erro: {error}')
        return threads

    def build_api_service(self):
        youtube_api_service_name, youtube_api_version, developer_key = self.get_credentials()
        return build(youtube_api_service_name, youtube_api_version, developerKey=developer_key)

    def load_comments_from_videoid_with_threads(self, videoid):
        youtube = self.build_api_service()
        video_comment_threads = self.get_comment_threads(youtube, videoid)
        start = 1
        end = len(video_comment_threads) + 1
        for thread in video_comment_threads:
            thread['comments'] = self.get_comments(youtube, thread['id'])
            start -= 1
            end -= 1
        return video_comment_threads
    
    def search_list(self, search, max_results):
        youtube = self.build_api_service()
        results = youtube.search().list(q=search, 
                                        part='id,snippet', 
                                        maxResults=max_results).execute()
        return results['items']
    
    def get_api_name(self):
        return 'YouTube'

def main():
    file_credentials = 'src/credentials.yaml'
    api = YouTubeAPI(file_credentials)
    videoid = 'fz5xFui6A_M'
    search = '#SUS #COVID'
    #video_comment_threads = api.load_comments_from_videoid_with_threads(videoid)
    search_list = api.search_list(search, 1)
    print(search_list)
    
if __name__ == '__main__':
    main()