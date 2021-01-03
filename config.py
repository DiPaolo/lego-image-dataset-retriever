import configparser
import sys

MAX_REST_API_REQUESTS = sys.maxsize
TOKEN = ''


def init_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if not config:
        print('WARNING Cannot read config.ini file with settings')
        return

    global MAX_REST_API_REQUESTS
    if 'debug' in config and 'MaxRESTApiRequests' in config['debug']:
        MAX_REST_API_REQUESTS = config['debug']['MaxRESTApiRequests']

    global TOKEN
    if 'rebrickable.com' in config and 'token' in config['rebrickable.com']:
        TOKEN = config['rebrickable.com']['token']
