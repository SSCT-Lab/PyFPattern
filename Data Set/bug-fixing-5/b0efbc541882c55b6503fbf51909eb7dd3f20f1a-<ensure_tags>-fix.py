def ensure_tags(vpc_conn, resource_id, tags, add_only, check_mode):
    try:
        cur_tags = get_resource_tags(vpc_conn, resource_id)
        if (cur_tags == tags):
            return {
                'changed': False,
                'tags': cur_tags,
            }
        if check_mode:
            latest_check_mode_tags = cur_tags
        to_delete = dict(((k, cur_tags[k]) for k in cur_tags if (k not in tags)))
        if (to_delete and (not add_only)):
            if check_mode:
                latest_check_mode_tags = dict(((k, cur_tags[k]) for k in cur_tags if (k not in to_delete)))
            else:
                vpc_conn.delete_tags(resource_id, to_delete)
        to_add = dict(((k, tags[k]) for k in tags if ((k not in cur_tags) or (cur_tags[k] != tags[k]))))
        if to_add:
            if check_mode:
                latest_check_mode_tags.update(to_add)
            else:
                vpc_conn.create_tags(resource_id, to_add)
        if check_mode:
            return {
                'changed': True,
                'tags': latest_check_mode_tags,
            }
        latest_tags = get_resource_tags(vpc_conn, resource_id)
        return {
            'changed': True,
            'tags': latest_tags,
        }
    except EC2ResponseError as e:
        raise AnsibleIGWException('Unable to update tags for {0}, error: {1}'.format(resource_id, e))