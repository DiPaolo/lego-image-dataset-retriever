import requests

import config
from entities.part import Part
from entities.part_category import PartCategory
from json_utils import get_json_value
from requests import HTTPError
from typing import List

_BASE_URL = 'https://rebrickable.com/'


def _get_request(endpoint: str) -> (object, str):
    try:
        r = requests.get(_BASE_URL + endpoint, headers={'Authorization': f'key {config.TOKEN}'})
    except HTTPError as http_err:
        return None, f'HTTP error occurred: {http_err}'
    except Exception as err:
        return None, f'Other error occurred: {err}'

    if r.status_code != 200:
        if r.status_code == 404:
            return None, f'Item not found'
        else:
            return None, f'Failed to receive data: HTTP status code is {r.status_code}'

    return r.json(), None


def get_part_categories() -> (List[PartCategory], str):
    json, err_msg = _get_request('/api/v3/lego/part_categories/')
    if json is None:
        return json, err_msg

    results = get_json_value(json, 'results')
    if results is None:
        return json, err_msg

    part_categories = []
    for result in results:
        part_categories.append(PartCategory(result))

    return part_categories, err_msg


def get_part_count() -> (int, str):
    json, err_msg = _get_request(f'/api/v3/lego/parts/?page=1&page_size=1')
    if json is None:
        return json, err_msg

    if json is None or 'count' not in json:
        return -1, err_msg

    return json['count'], None


def get_parts(page: int = 1, page_size: int = 100) -> (List[Part], str):
    json, err_msg = _get_request(f'/api/v3/lego/parts/?page={page}&page_size={page_size}')
    if json is None:
        return json, err_msg

    results = get_json_value(json, 'results')
    if results is None:
        return json, err_msg

    part_categories = []
    for result in results:
        part_categories.append(Part(result))

    return part_categories, err_msg


def get_part(part_id: int) -> (Part, str):
    json, err_msg = _get_request(f'/api/v3/lego/parts/{part_id}/')
    return Part(json), err_msg
