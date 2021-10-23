def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(subnet_id=dict(type='str'), eip_address=dict(type='str'), allocation_id=dict(type='str'), if_exist_do_not_create=dict(type='bool', default=False), state=dict(default='present', choices=['present', 'absent']), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=320, required=False), release_eip=dict(type='bool', default=False), nat_gateway_id=dict(type='str'), client_token=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[['allocation_id', 'eip_address']])
    if (not HAS_BOTO3):
        module.fail_json(msg='botocore/boto3 is required.')
    state = module.params.get('state').lower()
    check_mode = module.check_mode
    subnet_id = module.params.get('subnet_id')
    allocation_id = module.params.get('allocation_id')
    eip_address = module.params.get('eip_address')
    nat_gateway_id = module.params.get('nat_gateway_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    release_eip = module.params.get('release_eip')
    client_token = module.params.get('client_token')
    if_exist_do_not_create = module.params.get('if_exist_do_not_create')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        client = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=('Boto3 Client Error - ' + str(e.msg)))
    changed = False
    err_msg = ''
    if (state == 'present'):
        if (not subnet_id):
            module.fail_json(msg='subnet_id is required for creation')
        (success, changed, err_msg, results) = pre_create(client, subnet_id, allocation_id, eip_address, if_exist_do_not_create, wait, wait_timeout, client_token, check_mode=check_mode)
    elif (not nat_gateway_id):
        module.fail_json(msg='nat_gateway_id is required for removal')
    else:
        (success, changed, err_msg, results) = remove(client, nat_gateway_id, wait, wait_timeout, release_eip, check_mode=check_mode)
    if (not success):
        module.fail_json(msg=err_msg, success=success, changed=changed)
    else:
        module.exit_json(msg=err_msg, success=success, changed=changed, **results)