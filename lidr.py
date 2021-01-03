#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import commands.part
import commands.part_category
import configparser
import rba.api


def _read_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        token = config['rebrickable.com']['token']
        return token
    except:
        return None


if __name__ == '__main__':
    rba.api.set_token(_read_token())

    parser = argparse.ArgumentParser(description='LEGO')
    parser.add_argument('--print-part-categories', action=argparse.BooleanOptionalAction, help='prints all part categories')
    parser.add_argument('--print-part', metavar='ID', type=str, help='prints part info with specified ID')

    args = parser.parse_args()

    if 'print_part_categories' in args and args.print_part_categories:
        commands.part_category.print_all()
    elif 'print_part' in args and args.print_part:
        commands.part.print_info(args.print_part)
    else:
        parser.print_help()
