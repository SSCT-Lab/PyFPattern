def get_igw_info(igw):
    return {
        'gateway_id': igw.id,
        'tags': igw.tags,
        'vpc_id': igw.vpc_id,
    }