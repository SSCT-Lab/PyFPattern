def modify_eni(connection, vpc_id, module, eni):
    instance_id = module.params.get('instance_id')
    attached = module.params.get('attached')
    do_detach = (module.params.get('state') == 'detached')
    device_index = module.params.get('device_index')
    description = module.params.get('description')
    security_groups = module.params.get('security_groups')
    force_detach = module.params.get('force_detach')
    source_dest_check = module.params.get('source_dest_check')
    delete_on_termination = module.params.get('delete_on_termination')
    secondary_private_ip_addresses = module.params.get('secondary_private_ip_addresses')
    secondary_private_ip_address_count = module.params.get('secondary_private_ip_address_count')
    changed = False
    try:
        if (description is not None):
            if (eni.description != description):
                connection.modify_network_interface_attribute(eni.id, 'description', description)
                changed = True
        if (len(security_groups) > 0):
            groups = get_ec2_security_group_ids_from_names(security_groups, connection, vpc_id=vpc_id, boto3=False)
            if (sorted(get_sec_group_list(eni.groups)) != sorted(groups)):
                connection.modify_network_interface_attribute(eni.id, 'groupSet', groups)
                changed = True
        if (source_dest_check is not None):
            if (eni.source_dest_check != source_dest_check):
                connection.modify_network_interface_attribute(eni.id, 'sourceDestCheck', source_dest_check)
                changed = True
        if ((delete_on_termination is not None) and (eni.attachment is not None)):
            if (eni.attachment.delete_on_termination is not delete_on_termination):
                connection.modify_network_interface_attribute(eni.id, 'deleteOnTermination', delete_on_termination, eni.attachment.id)
                changed = True
        current_secondary_addresses = [i.private_ip_address for i in eni.private_ip_addresses if (not i.primary)]
        if (secondary_private_ip_addresses is not None):
            secondary_addresses_to_remove = list((set(current_secondary_addresses) - set(secondary_private_ip_addresses)))
            if secondary_addresses_to_remove:
                connection.unassign_private_ip_addresses(network_interface_id=eni.id, private_ip_addresses=list((set(current_secondary_addresses) - set(secondary_private_ip_addresses))), dry_run=False)
            connection.assign_private_ip_addresses(network_interface_id=eni.id, private_ip_addresses=secondary_private_ip_addresses, secondary_private_ip_address_count=None, allow_reassignment=False, dry_run=False)
        if (secondary_private_ip_address_count is not None):
            current_secondary_address_count = len(current_secondary_addresses)
            if (secondary_private_ip_address_count > current_secondary_address_count):
                connection.assign_private_ip_addresses(network_interface_id=eni.id, private_ip_addresses=None, secondary_private_ip_address_count=(secondary_private_ip_address_count - current_secondary_address_count), allow_reassignment=False, dry_run=False)
                changed = True
            elif (secondary_private_ip_address_count < current_secondary_address_count):
                secondary_addresses_to_remove_count = (current_secondary_address_count - secondary_private_ip_address_count)
                connection.unassign_private_ip_addresses(network_interface_id=eni.id, private_ip_addresses=current_secondary_addresses[:secondary_addresses_to_remove_count], dry_run=False)
        if (attached is True):
            if (eni.attachment and (eni.attachment.instance_id != instance_id)):
                detach_eni(eni, module)
                eni.attach(instance_id, device_index)
                wait_for_eni(eni, 'attached')
                changed = True
            if (eni.attachment is None):
                eni.attach(instance_id, device_index)
                wait_for_eni(eni, 'attached')
                changed = True
        elif (attached is False):
            detach_eni(eni, module)
    except BotoServerError as e:
        module.fail_json(msg=e.message)
    eni.update()
    module.exit_json(changed=changed, interface=get_eni_info(eni))