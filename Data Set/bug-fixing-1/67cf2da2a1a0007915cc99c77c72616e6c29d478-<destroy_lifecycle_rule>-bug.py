

def destroy_lifecycle_rule(client, module):
    name = module.params.get('name')
    prefix = module.params.get('prefix')
    rule_id = module.params.get('rule_id')
    changed = False
    if (prefix is None):
        prefix = ''
    try:
        current_lifecycle_rules = client.get_bucket_lifecycle_configuration(Bucket=name)['Rules']
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration'):
            current_lifecycle_rules = []
        else:
            module.fail_json_aws(e)
    except BotoCoreError as e:
        module.fail_json_aws(e)
    lifecycle_obj = dict(Rules=[])
    if (rule_id is not None):
        for existing_rule in current_lifecycle_rules:
            if (rule_id == existing_rule['ID']):
                changed = True
            else:
                lifecycle_obj['Rules'].append(existing_rule)
    else:
        for existing_rule in current_lifecycle_rules:
            if (prefix == existing_rule['Filter']['Prefix']):
                changed = True
            else:
                lifecycle_obj['Rules'].append(existing_rule)
    try:
        if lifecycle_obj['Rules']:
            client.put_bucket_lifecycle_configuration(Bucket=name, LifecycleConfiguration=lifecycle_obj)
        else:
            client.delete_lifecycle_configuration(Bucket=name)
    except (ClientError, BotoCoreError) as e:
        module.fail_json_aws(e)
    module.exit_json(changed=changed)
