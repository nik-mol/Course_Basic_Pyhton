import configparser
from file.vk import VKPhoto
from file.yandex import YandexDisk

config = configparser.ConfigParser()
config.read('setting.ini')

tokenVK = config['VK']['tokenVK']
tokenYAN = config['YAN']['tokenYAN']



if __name__ == '__main__': 
  
  vk_photo = VKPhoto(tokenVK, '5.131')
 
  
  yan = YandexDisk(token=tokenYAN)  
  yan.upload_file_to_disk(vk_photo.get_photo_from_vk())
 