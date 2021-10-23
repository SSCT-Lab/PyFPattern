def create_eni(connection, vpc_id, module):
    instance_id = module.params.get('instance_id')
    attached = module.params.get('attached')
    if (instance_id == 'None'):
        instance_id = None
    device_index = module.params.get('device_index')
    subnet_id = module.params.get('subnet_id')
    private_ip_address = module.params.get('private_ip_address')
    description = module.params.get('description')
    security_groups = get_ec2_security_group_ids_from_names(module.params.get('security_groups'), connection, vpc_id=vpc_id, boto3=False)
    secondary_private_ip_addresses = module.params.get('secondary_private_ip_addresses')
    secondary_private_ip_address_count = module.params.get('secondary_private_ip_address_count')
    changed = False
    try:
        eni = connection.create_network_interface(subnet_id, private_ip_address, description, security_groups)
        if (attached and (instance_id is not None)):
            try:
                eni.attach(instance_id, device_index)
            except BotoServerError:
                eni.delete()
                raise
            wait_for_eni(eni, 'attached')
            eni.update()
        if (secondary_private_ip_address_count is not None):
            try:
                connection.assign_private_ip_addresses(network_interface_id=eni.id, secondary_private_ip_address_count=secondary_private_ip_address_count)
            except BotoServerError:
                eni.delete()
                raise
        if (secondary_private_ip_addresses is not None):
            try:
                connection.assign_private_ip_addresses(network_interface_id=eni.id, private_ip_addresses=secondary_private_ip_addresses)
            except BotoServerError:
                eni.delete()
                raise
        changed = True
    except BotoServerError as e:
        module.fail_json(msg=e.message)
    module.exit_json(changed=changed, interface=get_eni_info(eni))