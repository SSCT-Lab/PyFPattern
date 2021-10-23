def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(query=dict(choices=['change', 'checker_ip_range', 'health_check', 'hosted_zone', 'record_sets', 'reusable_delegation_set'], required=True), change_id=dict(), hosted_zone_id=dict(), max_items=dict(type='str'), next_marker=dict(), delegation_set_id=dict(), start_record_name=dict(), type=dict(choices=['A', 'CNAME', 'MX', 'AAAA', 'TXT', 'PTR', 'SRV', 'SPF', 'CAA', 'NS']), dns_name=dict(), resource_id=dict(type='list', aliases=['resource_ids']), health_check_id=dict(), hosted_zone_method=dict(choices=['details', 'list', 'list_by_name', 'count', 'tags'], default='list'), health_check_method=dict(choices=['list', 'details', 'status', 'failure_reason', 'count', 'tags'], default='list')))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['hosted_zone_method', 'health_check_method']])
    if (not (HAS_BOTO or HAS_BOTO3)):
        module.fail_json(msg='json and boto/boto3 is required.')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        route53 = boto3_conn(module, conn_type='client', resource='route53', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=("Can't authorize connection - %s " % str(e)))
    invocations = {
        'change': change_details,
        'checker_ip_range': checker_ip_range_details,
        'health_check': health_check_details,
        'hosted_zone': hosted_zone_details,
        'record_sets': record_sets_details,
        'reusable_delegation_set': reusable_delegation_set_details,
    }
    results = invocations[module.params.get('query')](route53, module)
    module.exit_json(**results)