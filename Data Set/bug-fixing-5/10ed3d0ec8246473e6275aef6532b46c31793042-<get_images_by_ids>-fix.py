def get_images_by_ids(module, client, ids):
    images = []
    pool = get_all_images(client)
    for image in pool.IMAGE:
        if (str(image.ID) in ids):
            images.append(image)
            ids.remove(str(image.ID))
            if (len(ids) == 0):
                break
    if (len(ids) > 0):
        module.fail_json(msg=('There is no IMAGE(s) with id(s)=' + ', '.join(('{id}'.format(id=str(image_id)) for image_id in ids))))
    return images