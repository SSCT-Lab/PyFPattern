def ensure_present(ec2, module, domain, address, private_ip_address, device_id, reuse_existing_ip_allowed, check_mode, isinstance=True):
    changed = False
    if (not address):
        if check_mode:
            return {
                'changed': True,
            }
        address = allocate_address(ec2, domain, reuse_existing_ip_allowed)
        changed = True
    if device_id:
        if isinstance:
            instance = find_device(ec2, module, device_id)
            if reuse_existing_ip_allowed:
                if ((len(instance.vpc_id) > 0) and (domain is None)):
                    raise EIPException("You must set 'in_vpc' to true to associate an instance with an existing ip in a vpc")
            assoc_result = associate_ip_and_device(ec2, address, private_ip_address, device_id, check_mode)
        else:
            instance = find_device(ec2, module, device_id, isinstance=False)
            assoc_result = associate_ip_and_device(ec2, address, private_ip_address, device_id, check_mode, isinstance=False)
        if instance.vpc_id:
            domain = 'vpc'
        changed = (changed or assoc_result['changed'])
    return {
        'changed': changed,
        'public_ip': address.public_ip,
        'allocation_id': address.allocation_id,
    }