def update_key(connection, module, key):
    changed = False
    alias = module.params['alias']
    if (not alias.startswith('alias/')):
        alias = ('alias/' + alias)
    aliases = get_kms_aliases_with_backoff(connection)['Aliases']
    key_id = module.params.get('key_id')
    if key_id:
        if (alias not in [_alias['AliasName'] for _alias in aliases]):
            try:
                connection.create_alias(KeyId=key_id, AliasName=alias)
                changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(msg='Failed create key alias')
    if (key['key_state'] == 'PendingDeletion'):
        try:
            connection.cancel_key_deletion(KeyId=key['key_id'])
            key['key_state'] = 'Disabled'
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Failed to cancel key deletion')
    changed = (ensure_enabled_disabled(connection, module, key) or changed)
    description = module.params.get('description')
    if (description and (key['description'] != description)):
        try:
            connection.update_key_description(KeyId=key['key_id'], Description=description)
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Failed to update key description')
    desired_tags = module.params.get('tags')
    (to_add, to_remove) = compare_aws_tags(key['tags'], desired_tags, module.params.get('purge_tags'))
    if to_remove:
        try:
            connection.untag_resource(KeyId=key['key_id'], TagKeys=to_remove)
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Unable to remove or update tag')
    if to_add:
        try:
            connection.tag_resource(KeyId=key['key_id'], Tags=[{
                'TagKey': tag_key,
                'TagValue': desired_tags[tag_key],
            } for tag_key in to_add])
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Unable to add tag to key')
    desired_grants = module.params.get('grants')
    existing_grants = key['grants']
    (to_add, to_remove) = compare_grants(existing_grants, desired_grants, module.params.get('purge_grants'))
    if to_remove:
        for grant in to_remove:
            try:
                connection.retire_grant(KeyId=key['key_arn'], GrantId=grant['grant_id'])
                changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg='Unable to retire grant')
    if to_add:
        for grant in to_add:
            grant_params = convert_grant_params(grant, key)
            try:
                connection.create_grant(**grant_params)
                changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg='Unable to create grant')
    result = get_key_details(connection, module, key['key_id'])
    module.exit_json(changed=changed, **camel_dict_to_snake_dict(result))