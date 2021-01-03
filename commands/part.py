import config
import rba.api


def print_parts():
    page_size = config.REST_API_PAGE_SIZE
    cur_page = 1
    part_count, err_msg = rba.api.get_part_count()
    if err_msg:
        print(f'ERROR Failed to get total part count. {err_msg}')
        return

    last_page = min(part_count // page_size + 1, config.MAX_REST_API_REQUESTS)
    while cur_page <= last_page:
        parts, err_msg = rba.api.get_parts(cur_page, page_size)
        if parts is None:
            print(f'ERROR Failed to get list of parts. {err_msg}')
            return

        for part in parts:
            print(f"  {part.part_num()}: {part.name()} ({part.image_url()})")

        cur_page += 1


def print_part(part_id: int):
    part, err_msg = rba.api.get_part(part_id)
    if part is None:
        print(f'ERROR Failed to get part. {err_msg}')
        return

    print(f"{part_id}: {part.name()} ({part.image_url()})")
