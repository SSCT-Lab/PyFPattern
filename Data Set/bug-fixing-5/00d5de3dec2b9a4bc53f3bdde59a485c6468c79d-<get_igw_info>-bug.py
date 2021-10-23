def get_igw_info(igw):
    return {
        'id': igw.id,
        'tags': igw.tags,
        'vpc_id': igw.vpc_id,
    }