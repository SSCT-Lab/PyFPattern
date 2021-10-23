def find_eni(connection, module):
    eni_id = module.params.get('eni_id')
    subnet_id = module.params.get('subnet_id')
    private_ip_address = module.params.get('private_ip_address')
    instance_id = module.params.get('instance_id')
    device_index = module.params.get('device_index')
    try:
        filters = {
            
        }
        if subnet_id:
            filters['subnet-id'] = subnet_id
        if private_ip_address:
            filters['private-ip-address'] = private_ip_address
        else:
            if instance_id:
                filters['attachment.instance-id'] = instance_id
            if device_index:
                filters['attachment.device-index'] = device_index
        eni_result = connection.get_all_network_interfaces(eni_id, filters=filters)
        if (len(eni_result) == 1):
            return eni_result[0]
        else:
            return None
    except BotoServerError as e:
        module.fail_json(msg=e.message)
    return None