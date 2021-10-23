def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(eni_id=dict(default=None, type='str'), instance_id=dict(default=None, type='str'), private_ip_address=dict(type='str'), subnet_id=dict(type='str'), description=dict(type='str'), security_groups=dict(default=[], type='list'), device_index=dict(default=0, type='int'), state=dict(default='present', choices=['present', 'absent']), force_detach=dict(default='no', type='bool'), source_dest_check=dict(default=None, type='bool'), delete_on_termination=dict(default=None, type='bool'), secondary_private_ip_addresses=dict(default=None, type='list'), secondary_private_ip_address_count=dict(default=None, type='int'), attached=dict(default=None, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['secondary_private_ip_addresses', 'secondary_private_ip_address_count']], required_if=[('state', 'absent', ['eni_id']), ('attached', True, ['instance_id'])])
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if region:
        try:
            connection = connect_to_aws(boto.ec2, region, **aws_connect_params)
            vpc_connection = connect_to_aws(boto.vpc, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    else:
        module.fail_json(msg='region must be specified')
    state = module.params.get('state')
    if (state == 'present'):
        eni = uniquely_find_eni(connection, module)
        if (eni is None):
            subnet_id = module.params.get('subnet_id')
            if (subnet_id is None):
                module.fail_json(msg='subnet_id is required when creating a new ENI')
            vpc_id = _get_vpc_id(vpc_connection, module, subnet_id)
            create_eni(connection, vpc_id, module)
        else:
            vpc_id = eni.vpc_id
            modify_eni(connection, vpc_id, module, eni)
    elif (state == 'absent'):
        delete_eni(connection, module)