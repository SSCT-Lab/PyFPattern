def ensure_igw_present(vpc_conn, vpc_id, tags, check_mode):
    igw = get_matching_igw(vpc_conn, vpc_id)
    changed = False
    if (igw is None):
        if check_mode:
            return {
                'changed': True,
                'gateway_id': None,
            }
        try:
            igw = vpc_conn.create_internet_gateway()
            vpc_conn.attach_internet_gateway(igw.id, vpc_id)
            changed = True
        except EC2ResponseError as e:
            raise AnsibleIGWException('Unable to create Internet Gateway, error: {0}'.format(e))
    igw.vpc_id = vpc_id
    if (tags != igw.tags):
        if check_mode:
            check_mode_tags = ensure_tags(vpc_conn, igw.id, tags, False, check_mode)
            igw_info = get_igw_info(igw)
            igw_info.get('tags', {
                
            }).update(check_mode_tags.get('tags', {
                
            }))
            return {
                'changed': True,
                'gateway': igw_info,
            }
        ensure_tags(vpc_conn, igw.id, tags, False, check_mode)
        igw.tags = tags
        changed = True
    igw_info = get_igw_info(igw)
    return {
        'changed': changed,
        'gateway': igw_info,
    }