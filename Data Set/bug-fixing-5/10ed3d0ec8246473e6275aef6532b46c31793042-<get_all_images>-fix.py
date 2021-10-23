def get_all_images(client):
    pool = client.imagepool.info((- 2), (- 1), (- 1), (- 1))
    return pool