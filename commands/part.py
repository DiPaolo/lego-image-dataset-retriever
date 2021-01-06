import config
import os

import db
import rba.api
from entities.part import Part
from entities.part_image import PartImage
from pathlib import Path


def _iterate_parts(callback, print_cat_id: int = None, progress_callback = None):
    page_size = config.REST_API_PAGE_SIZE
    cur_page = 0
    total_part_count, err_msg = rba.api.get_part_count(print_cat_id)
    if err_msg:
        print(f'ERROR Failed to get total part count. {err_msg}')
        return

    if total_part_count // page_size + 1 > config.MAX_REST_API_REQUESTS:
        print(f'WARNING {config.MAX_REST_API_REQUESTS * page_size} of {total_part_count} parts will be processed. '
              f'You may change the maximum count of parts to be printed in config.ini.')
        last_page = config.MAX_REST_API_REQUESTS
        part_count_to_download = config.MAX_REST_API_REQUESTS * page_size
    else:
        last_page = total_part_count // page_size + 1
        part_count_to_download = total_part_count

    downloaded_image_count = 0
    while cur_page < last_page:
        parts, err_msg = rba.api.get_parts(cur_page + 1, page_size, print_cat_id)
        if parts is None:
            print(f'ERROR Failed to get list of parts. {err_msg}')
            return

        for part in parts:
            callback(part)
            downloaded_image_count += 1
            if progress_callback:
                progress_callback(downloaded_image_count, part_count_to_download)

        cur_page += 1

    progress_callback(cur_page * page_size, part_count_to_download)


def print_parts(print_cat_id: int = None, progress_callback = None):
    _iterate_parts(print_cat_id=print_cat_id,
                   callback=lambda part: print(f"  {part.part_num()}: {part.name()} ({part.image_url()})"),
                   progress_callback=progress_callback)


def print_part(part_id: int):
    part, err_msg = rba.api.get_part(part_id)
    if part is None:
        print(f'ERROR Failed to get part. {err_msg}')
        return

    print(f"{part_id}: {part.name()} ({part.image_url()})")


def download_parts_images(print_cat_id: int = None, out_dir: str = os.path.curdir, progress_callback = None):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    _iterate_parts(print_cat_id=print_cat_id, callback=lambda part: _download_part_image(part, out_dir),
                   progress_callback=progress_callback)


def _download_part_image(part: Part, out_dir: str = os.path.curdir):
    new_part_id = db.add_part(part)

    # some parts have no images
    part_img = PartImage(part.image_url())
    if part_img:
        part_img.download(out_dir)
        db.add_part_image(new_part_id, part_img)


def print_parts_stats(print_cat_id: int = None):
    res_stats = db.fetch_resolutions(print_cat_id)

    total_img_count = sum(res_stats.values())

    for res in sorted(res_stats.items(), key=lambda item: item[1], reverse=True):
        print(f'{res[0][0]}x{res[0][1]} - {res[1]} ({res[1] / total_img_count * 100.0:.1f}%)')
