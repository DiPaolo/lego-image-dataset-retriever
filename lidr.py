#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import commands.part
import commands.part_category

import config


if __name__ == '__main__':
    config.init_config()

    parser = argparse.ArgumentParser(description='LEGO')
    parser.add_argument('--print-part-categories', action=argparse.BooleanOptionalAction, help='print all part categories')
    parser.add_argument('--print-part', metavar='ID', type=str, help='print part info with specified ID')
    parser.add_argument('--print-parts', action=argparse.BooleanOptionalAction, help='print information for specified parts')

    args = parser.parse_args()

    if 'print_part_categories' in args and args.print_part_categories:
        commands.part_category.print_all()
    elif 'print_part' in args and args.print_part:
        commands.part.print_part(args.print_part)
    elif 'print_parts' in args and args.print_parts:
        commands.part.print_parts()
    else:
        parser.print_help()
