from json_utils import get_json_value


class Part(object):
    def __new__(cls, json_object):
        if json_object:
            return super(Part, cls).__new__(cls)
        else:
            return None

    def __init__(self, json_object):
        self.__json = json_object

    def part_num(self):
        return get_json_value(self.__json, 'part_num')

    def name(self):
        return get_json_value(self.__json, 'name')

    def image_url(self):
        return get_json_value(self.__json, 'part_img_url')
