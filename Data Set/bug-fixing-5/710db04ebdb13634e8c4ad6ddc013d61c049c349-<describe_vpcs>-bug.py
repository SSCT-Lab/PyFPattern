def describe_vpcs(connection, module):
    '\n    Describe VPCs.\n\n    connection  : boto3 client connection object\n    module  : AnsibleModule object\n    '
    filters = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    vpc_ids = module.params.get('vpc_ids')
    vpc_info = list()
    vpc_list = list()
    try:
        response = connection.describe_vpcs(VpcIds=vpc_ids, Filters=filters)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for vpc in response['Vpcs']:
        vpc_list.append(vpc['VpcId'])
    try:
        cl_enabled = connection.describe_vpc_classic_link(VpcIds=vpc_list)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    try:
        cl_dns_support = connection.describe_vpc_classic_link_dns_support(VpcIds=vpc_list)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for vpc in response['Vpcs']:
        try:
            dns_support = describe_vpc_attr_with_backoff(connection, vpc['VpcId'], 'enableDnsSupport')
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        try:
            dns_hostnames = describe_vpc_attr_with_backoff(connection, vpc['VpcId'], 'enableDnsHostnames')
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        for item in cl_enabled['Vpcs']:
            if (vpc['VpcId'] == item['VpcId']):
                vpc['ClassicLinkEnabled'] = item['ClassicLinkEnabled']
        for item in cl_dns_support['Vpcs']:
            if (vpc['VpcId'] == item['VpcId']):
                vpc['ClassicLinkDnsSupported'] = item['ClassicLinkDnsSupported']
        vpc['EnableDnsSupport'] = dns_support['EnableDnsSupport'].get('Value')
        vpc['EnableDnsHostnames'] = dns_hostnames['EnableDnsHostnames'].get('Value')
        vpc['id'] = vpc['VpcId']
        vpc_info.append(camel_dict_to_snake_dict(vpc))
        vpc_info[(- 1)]['tags'] = boto3_tag_list_to_ansible_dict(vpc.get('Tags', []))
    module.exit_json(vpcs=vpc_info)