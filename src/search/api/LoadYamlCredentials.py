import yaml
from yaml.loader import SafeLoader

class LoadYamlCredentials:
    def __init__(self, file_name_credentials):
        self.file_name_credentials = file_name_credentials

    def get_credentials(self, *argv):
        with open(self.file_name_credentials) as f:
            dict = {}
            data = yaml.load(f, Loader=SafeLoader)
            for arg in argv:
                dict[arg] = data[arg]
            return dict 

    def get_list_of_params_yaml(self, list_params, index):
        print('list_params', list_params)
        if isinstance(list_params, list):
            return list_params[index]
        else:
            list_params

def main():
    file_credentials = 'src/search/api/teste_credentials.yaml'
    cred = LoadYamlCredentials(file_credentials)
    dict = cred.get_credentials('youtube_api_service_name', 'youtube_api_version', 'developer_key')
    print(dict['developer_key'][0])

if __name__ == '__main__':
    main()