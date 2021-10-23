def describe_subnets(connection, module):
    '\n    Describe Subnets.\n\n    module  : AnsibleModule object\n    connection  : boto3 client connection object\n    '
    filters = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    subnet_ids = module.params.get('subnet_ids')
    if (subnet_ids is None):
        subnet_ids = []
    subnet_info = list()
    try:
        response = describe_subnets_with_backoff(connection, subnet_ids, filters)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for subnet in response['Subnets']:
        subnet['id'] = subnet['SubnetId']
        subnet_info.append(camel_dict_to_snake_dict(subnet))
        subnet_info[(- 1)]['tags'] = boto3_tag_list_to_ansible_dict(subnet.get('Tags', []))
    module.exit_json(subnets=subnet_info)