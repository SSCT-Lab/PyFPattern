def ensure_tags(vpc_conn, resource_id, tags, add_only, check_mode):
    try:
        cur_tags = get_resource_tags(vpc_conn, resource_id)
        if (tags == cur_tags):
            return {
                'changed': False,
                'tags': cur_tags,
            }
        to_delete = dict(((k, cur_tags[k]) for k in cur_tags if (k not in tags)))
        if (to_delete and (not add_only)):
            vpc_conn.delete_tags(resource_id, to_delete, dry_run=check_mode)
        to_add = dict(((k, tags[k]) for k in tags if (k not in cur_tags)))
        if to_add:
            vpc_conn.create_tags(resource_id, to_add, dry_run=check_mode)
        latest_tags = get_resource_tags(vpc_conn, resource_id)
        return {
            'changed': True,
            'tags': latest_tags,
        }
    except EC2ResponseError as e:
        raise AnsibleTagCreationException(message='Unable to update tags for {0}, error: {1}'.format(resource_id, e), error_traceback=traceback.format_exc())