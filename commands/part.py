import rba.api


def print_info(part_id: int):
    part, err_msg = rba.api.get_part(part_id)
    if part is None:
        print(f'ERROR Failed to get part. {err_msg}')
        return

    print(f"{part_id}: {part.name()} ({part.image_url()})")
