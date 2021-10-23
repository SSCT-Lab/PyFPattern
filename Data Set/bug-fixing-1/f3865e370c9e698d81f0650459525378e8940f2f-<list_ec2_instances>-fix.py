

def list_ec2_instances(connection, module):
    instance_ids = module.params.get('instance_ids')
    filters = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    try:
        reservations_paginator = connection.get_paginator('describe_instances')
        reservations = reservations_paginator.paginate(InstanceIds=instance_ids, Filters=filters).build_full_result()
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    instances = []
    for reservation in reservations['Reservations']:
        instances = (instances + reservation['Instances'])
    snaked_instances = [camel_dict_to_snake_dict(instance) for instance in instances]
    for instance in snaked_instances:
        instance['tags'] = boto3_tag_list_to_ansible_dict(instance.get('tags', []), 'key', 'value')
    module.exit_json(instances=snaked_instances)
