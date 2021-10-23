def list_dhcp_options(client, module):
    params = dict(Filters=ansible_dict_to_boto3_filter_list(module.params.get('filters')))
    if module.params.get('dry_run'):
        params['DryRun'] = True
    if module.params.get('dhcp_options_ids'):
        params['DhcpOptionsIds'] = module.params.get('dhcp_options_ids')
    try:
        all_dhcp_options = client.describe_dhcp_options(**params)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    results = [camel_dict_to_snake_dict(get_dhcp_options_info(option)) for option in all_dhcp_options['DhcpOptions']]
    module.exit_json(dhcp_options=results)