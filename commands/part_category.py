from pprint import pprint

import db
import rba.api


def print_all():
    part_categories, err_msg = rba.api.get_part_categories()
    if part_categories is None:
        print(f'ERROR Failed to get list of part categories. {err_msg}')
        return

    for part_category in part_categories:
        db.add_part_category(part_category)
        print(f'  {part_category.id()}: {part_category.name()} ({part_category.rba_part_count()})')


def print_part_cats_stats():
    res_stats = db.fetch_categories()

    total_img_count = sum([v['count'] for k, v in res_stats.items()])

    print(f'Total {total_img_count} images:')
    for res in sorted(res_stats.items(), key=lambda item: item[1]['count'], reverse=True):
        print(f"  {res[1]['name']} (id={res[0]}) - {res[1]['count']} ({res[1]['count'] / total_img_count * 100.0:.1f}%)")
