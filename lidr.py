#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import commands.part
import commands.part_category
import config
import tqdm

if __name__ == '__main__':
    config.init_config()

    parser = argparse.ArgumentParser(description='LEGO')
    parser.add_argument('--print-part-categories', action=argparse.BooleanOptionalAction, help='print all part categories')
    parser.add_argument('--print-part', metavar='ID', type=str, help='print part info with specified ID')
    parser.add_argument('--print-parts', action=argparse.BooleanOptionalAction, help='print information for specified parts')
    parser.add_argument('--download-parts-images', action=argparse.BooleanOptionalAction, help='download images of specified parts')
    parser.add_argument('--part-category-id', metavar='ID', type=int, help='specify part category ID')
    parser.add_argument('--output-dir', metavar='dir', type=str, help='directory where the output will be stored to')

    args = parser.parse_args()

    print_cat_id = args.part_category_id if 'part_category_id' in args else None
    out_dir = args.output_dir if 'output_dir' in args else None

    if 'print_part_categories' in args and args.print_part_categories:
        commands.part_category.print_all()
    elif 'print_part' in args and args.print_part:
        commands.part.print_part(args.print_part)
    elif 'print_parts' in args and args.print_parts:
        commands.part.print_parts(print_cat_id)
    elif 'download_parts_images' in args and args.download_parts_images:
        def update_progress_bar(cur_value: int, total: int):
            if not hasattr(update_progress_bar, 'pb'):
                update_progress_bar.pb = tqdm.tqdm(total=total, desc='Downloading images', unit='img')
                update_progress_bar.last_num = 0

            update_progress_bar.pb.update(cur_value - update_progress_bar.last_num)
            update_progress_bar.last_num = cur_value

        commands.part.download_parts_images(print_cat_id, out_dir, lambda cur, total: update_progress_bar(cur, total))
    else:
        parser.print_help()
