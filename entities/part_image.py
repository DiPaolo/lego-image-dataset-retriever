from PIL import Image
import os
import requests
from requests import HTTPError
from urllib.parse import urlparse


class PartImage(object):
    def __new__(cls, json_object):
        if json_object:
            return super(PartImage, cls).__new__(cls)
        else:
            return None

    def __init__(self, url):
        self.__url = url
        self.__w = 0
        self.__h = 0
        self.__downloaded_filename = None

    def image_url(self):
        return self.__url

    def download(self, out_dir: str):
        try:
            r = requests.get(self.__url, allow_redirects=True)

            base_name = os.path.basename(urlparse(self.__url).path)
            filename = os.path.join(out_dir, base_name)
            open(filename, 'wb').write(r.content)

            self.__downloaded_filename = filename

            image = Image.open(self.__downloaded_filename)
            self.__w, self.__h = image.size
        except HTTPError as http_err:
            print(f'ERROR Failed to download {self.__url}. HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'ERROR Failed to download {self.__url}. {err}')
        except:
            print(f'ERROR Failed to download {self.__url}. Reason is unknown.')

        return self.__downloaded_filename

    def width(self):
        return self.__w

    def height(self):
        return self.__h

    def downloaded_filename(self):
        return self.__downloaded_filename

    def is_downloaded(self) -> bool:
        return self.__downloaded_filename is not None
