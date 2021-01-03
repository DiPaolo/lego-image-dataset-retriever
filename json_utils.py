def get_json_value(json, key: str):
    if not json or key not in json:
        return None
    else:
        return json[key]
