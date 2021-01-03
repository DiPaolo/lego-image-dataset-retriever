from json_utils import get_json_value


class PartCategory(object):
    def __new__(cls, json_object):
        if json_object:
            return super(PartCategory, cls).__new__(cls)
        else:
            return None

    def __init__(self, json_object):
        self.__json = json_object

    def id(self):
        return get_json_value(self.__json, 'id')

    def name(self):
        return get_json_value(self.__json, 'name')

    def part_count(self):
        return get_json_value(self.__json, 'part_count')
