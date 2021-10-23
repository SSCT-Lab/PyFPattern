def get_reservations(module, ec2, vpc, tags=None, state=None, zone=None):
    filters = dict()
    vpc_subnet_id = module.params.get('vpc_subnet_id')
    vpc_id = None
    if vpc_subnet_id:
        filters.update({
            'subnet-id': vpc_subnet_id,
        })
        if vpc:
            vpc_id = vpc.get_all_subnets(subnet_ids=[vpc_subnet_id])[0].vpc_id
    if vpc_id:
        filters.update({
            'vpc-id': vpc_id,
        })
    if (tags is not None):
        if isinstance(tags, str):
            try:
                tags = literal_eval(tags)
            except:
                pass
        if isinstance(tags, str):
            filters.update({
                'tag-key': tags,
            })
        if isinstance(tags, list):
            for x in tags:
                if isinstance(x, dict):
                    x = _set_none_to_blank(x)
                    filters.update(dict(((('tag:' + tn), tv) for (tn, tv) in x.items())))
                else:
                    filters.update({
                        'tag-key': x,
                    })
        if isinstance(tags, dict):
            tags = _set_none_to_blank(tags)
            filters.update(dict(((('tag:' + tn), tv) for (tn, tv) in tags.items())))
    if state:
        filters.update({
            'instance-state-name': state,
        })
    if zone:
        filters.update({
            'availability-zone': zone,
        })
    results = ec2.get_all_instances(filters=filters)
    return results