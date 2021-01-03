import rba.api


def print_all():
    part_categories, err_msg = rba.api.get_part_categories()
    if part_categories is None:
        print(f'ERROR Failed to get list of part categories. {err_msg}')
        return

    for part_category in part_categories:
        print(f'  {part_category.id()}: {part_category.name()} ({part_category.part_count()})')
