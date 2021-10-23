def paginated_list(s3, **pagination_params):
    pg = s3.get_paginator('list_objects_v2')
    for page in pg.paginate(**pagination_params):
        (yield [data['Key'] for data in page.get('Contents', [])])