import requests
import json
import time 
from pprint import pprint

class VKPhoto:
  url = 'https://api.vk.com/method/'
  def __init__(self, tokenVK, version):
    self.params = {
      'access_token': tokenVK,
      'v': version
    }

  def get_user_id(self, user_id = input('Введите ID пользователя: ')):
    user_url = self.url + 'users.get'
    user_params = {
      'user_ids': user_id
    }
    data_user_id = requests.get(user_url, params = {**self.params, **user_params}).json()['response'][0]['id']
    return data_user_id

  def get_alboms(self):
    dict_albom_id ={}
    user_id = self.get_user_id()
    list_alboms_url = self.url + 'photos.getAlbums'
    list_alboms_params = {
      'owner_id': user_id
    }
    response = requests.get(list_alboms_url, params = {**self.params, **list_alboms_params}).json()['response']['items']
    for i in response:
      dict_albom_id[i['title']]= i['id']    
    return dict_albom_id
   
  def get_photo_from_vk(self): 
    account = self.get_user_id()
    pprint(self.get_alboms())
    album_id = input('Введите ID альбома из списка: ')
    count = input('Введите количество фотографий для загрузки : ')
    if count == '':
      count = 5
    photo_url = self.url + 'photos.get'
    photo_params = {    
      'count': count,      
      'owner_id': account,
      'album_id': album_id, 
      'extended': 1,
      'photo_sizes': 1, 
      'rev': 1
    }
    data_fotos = requests.get(photo_url, params = {**self.params, **photo_params}).json()['response']['items'] 
      
    dict_foto = {}
    log_data = []
    for data_foto in data_fotos:
      file_name = data_foto['likes']['count']
      file_date = time.strftime('%Y%B%d%A%H_%M_%S', time.localtime(data_foto['date']))
      file_url = data_foto['sizes'][-1]['url']
      file_size = data_foto['sizes'][-1]['type']
      if file_name not in dict_foto.keys():
        dict_foto[file_name] = file_url
        log_data.append({'file_name': f'{file_name}.jpg', 'size': file_size}) 
      else: 
        dict_foto[f'{file_name} -- {file_date}'] = file_url
        log_data.append({'file_name': f'{file_name}.jpg | {file_date}', 'size': file_size}) 
    with open('log.json', 'w') as file_log:    
      json.dump(log_data, file_log, indent=4)  
 
    return dict_foto
