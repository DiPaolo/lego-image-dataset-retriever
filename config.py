import configparser
import sys

TOKEN = ''
MAX_REST_API_REQUESTS = sys.maxsize
REST_API_PAGE_SIZE = 100


def init_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if not config:
        print('WARNING Cannot read config.ini file with settings')
        return

    global TOKEN
    if 'rebrickable.com' in config and 'token' in config['rebrickable.com']:
        TOKEN = config['rebrickable.com']['token']

    global MAX_REST_API_REQUESTS
    if 'debug' in config and 'MaxRESTApiRequests' in config['debug']:
        MAX_REST_API_REQUESTS = int(config['debug']['MaxRESTApiRequests'])

    global REST_API_PAGE_SIZE
    if 'debug' in config and 'RESTApiPageSize' in config['debug']:
        REST_API_PAGE_SIZE = int(config['debug']['RESTApiPageSize'])
