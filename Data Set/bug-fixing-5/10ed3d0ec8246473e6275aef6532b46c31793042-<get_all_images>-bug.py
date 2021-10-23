def get_all_images(client):
    pool = oca.ImagePool(client)
    pool.info(filter=(- 2))
    return pool