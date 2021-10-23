def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(device_id=dict(required=False, aliases=['instance_id']), public_ip=dict(required=False, aliases=['ip']), state=dict(required=False, default='present', choices=['present', 'absent']), in_vpc=dict(required=False, type='bool', default=False), reuse_existing_ip_allowed=dict(required=False, type='bool', default=False), release_on_disassociation=dict(required=False, type='bool', default=False), wait_timeout=dict(default=300), private_ip_address=dict(required=False, default=None, type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    ec2 = ec2_connect(module)
    device_id = module.params.get('device_id')
    instance_id = module.params.get('instance_id')
    public_ip = module.params.get('public_ip')
    private_ip_address = module.params.get('private_ip_address')
    state = module.params.get('state')
    in_vpc = module.params.get('in_vpc')
    domain = ('vpc' if in_vpc else None)
    reuse_existing_ip_allowed = module.params.get('reuse_existing_ip_allowed')
    release_on_disassociation = module.params.get('release_on_disassociation')
    if ((private_ip_address is not None) and (device_id is None)):
        module.fail_json(msg="parameters are required together: ('device_id', 'private_ip_address')")
    if instance_id:
        warnings = ['instance_id is no longer used, please use device_id going forward']
        is_instance = True
        device_id = instance_id
    elif (device_id and device_id.startswith('i-')):
        is_instance = True
    elif device_id:
        if (device_id.startswith('eni-') and (not in_vpc)):
            module.fail_json(msg='If you are specifying an ENI, in_vpc must be true')
        is_instance = False
    try:
        if device_id:
            address = find_address(ec2, public_ip, device_id, isinstance=is_instance)
        else:
            address = find_address(ec2, public_ip, None)
        if (state == 'present'):
            if device_id:
                result = ensure_present(ec2, module, domain, address, private_ip_address, device_id, reuse_existing_ip_allowed, module.check_mode, isinstance=is_instance)
            else:
                if address:
                    changed = False
                else:
                    (address, changed) = allocate_address(ec2, domain, reuse_existing_ip_allowed)
                result = {
                    'changed': changed,
                    'public_ip': address.public_ip,
                    'allocation_id': address.allocation_id,
                }
        elif device_id:
            disassociated = ensure_absent(ec2, domain, address, device_id, module.check_mode, isinstance=is_instance)
            if (release_on_disassociation and disassociated['changed']):
                released = release_address(ec2, address, module.check_mode)
                result = {
                    'changed': True,
                    'disassociated': disassociated,
                    'released': released,
                }
            else:
                result = {
                    'changed': disassociated['changed'],
                    'disassociated': disassociated,
                    'released': {
                        'changed': False,
                    },
                }
        else:
            released = release_address(ec2, address, module.check_mode)
            result = {
                'changed': released['changed'],
                'disassociated': {
                    'changed': False,
                },
                'released': released,
            }
    except (boto.exception.EC2ResponseError, EIPException) as e:
        module.fail_json(msg=str(e))
    if instance_id:
        result['warnings'] = warnings
    module.exit_json(**result)