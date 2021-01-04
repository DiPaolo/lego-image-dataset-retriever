from requests import HTTPError

import config
import os
import requests
import rba.api
from entities.part import Part
from pathlib import Path
from urllib.parse import urlparse


def _iterate_parts(callback, print_cat_id: int = None):
    page_size = config.REST_API_PAGE_SIZE
    cur_page = 1
    part_count, err_msg = rba.api.get_part_count(print_cat_id)
    if err_msg:
        print(f'ERROR Failed to get total part count. {err_msg}')
        return

    if part_count // page_size + 1 > config.MAX_REST_API_REQUESTS:
        print(f'WARNING {config.MAX_REST_API_REQUESTS * page_size} of {part_count} parts will be printed.'
              f'You may change the maximum count of parts to be printed in config.ini.')
        last_page = config.MAX_REST_API_REQUESTS
    else:
        last_page = part_count // page_size + 1

    while cur_page <= last_page:
        parts, err_msg = rba.api.get_parts(cur_page, page_size, print_cat_id)
        if parts is None:
            print(f'ERROR Failed to get list of parts. {err_msg}')
            return

        for part in parts:
            callback(part)

        cur_page += 1


def print_parts(print_cat_id: int = None):
    _iterate_parts(print_cat_id=print_cat_id, callback=lambda part: print(f"  {part.part_num()}: {part.name()} ({part.image_url()})"))


def print_part(part_id: int):
    part, err_msg = rba.api.get_part(part_id)
    if part is None:
        print(f'ERROR Failed to get part. {err_msg}')
        return

    print(f"{part_id}: {part.name()} ({part.image_url()})")


def download_parts_images(print_cat_id: int = None, out_dir: str = os.path.curdir):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    _iterate_parts(print_cat_id=print_cat_id, callback=lambda part: _download_part(part, out_dir))


def _download_part(part: Part, out_dir: str = os.path.curdir):
    try:
        r = requests.get(part.image_url(), allow_redirects=True)
        filename = os.path.basename(urlparse(part.image_url()).path)
        open(os.path.join(out_dir, filename), 'wb').write(r.content)
    except HTTPError as http_err:
        print(f'ERROR Failed to download {part.image_url()}. HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'ERROR Failed to download {part.image_url()}. {err}')
    except:
        print(f'ERROR Failed to download {part.image_url()}. Reason is unknown.')
