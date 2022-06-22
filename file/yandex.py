import requests
from progress.bar import IncrementalBar

class YandexDisk:

    def __init__(self, token):
      self.token = token     

    def get_headers(self):
      return {
        'Content-Type': 'application/json',
        'Authorization': self.token
      }

    def create_directory(self, name_directory=''):
      name_directory = input('Введите имя папки: ')
      headers = self.get_headers()     
      params = {
        'path': name_directory
      }
      response = requests.put(url = 'https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers).json() 
      result = response.get('href').split('%3A%2F')[1]    
      return result   
     
    def upload_file_to_disk(self, file):
        directory = self.create_directory()        
        headers = self.get_headers() 
        bar = IncrementalBar('files upload', max = len(file))            
        for name, value in file.items():
          params = {
            'path': f'{directory}/{name}',
            'url': f'{value}'
          }  
          response = requests.post(url = "https://cloud-api.yandex.net/v1/disk/resources/upload", params=params, headers=headers)
          bar.next() 
        bar.finish()
        response.raise_for_status()
        if response.status_code == 202:
          print('\n Success')
        return response