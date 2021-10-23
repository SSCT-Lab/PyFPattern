

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(instance=dict(), id=dict(), name=dict(), volume_size=dict(), volume_type=dict(choices=['standard', 'gp2', 'io1', 'st1', 'sc1'], default='standard'), iops=dict(), encrypted=dict(type='bool', default=False), kms_key_id=dict(), device_name=dict(), delete_on_termination=dict(type='bool', default=False), zone=dict(aliases=['availability_zone', 'aws_zone', 'ec2_zone']), snapshot=dict(), state=dict(choices=['absent', 'present', 'list'], default='present'), tags=dict(type='dict', default={
        
    })))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    id = module.params.get('id')
    name = module.params.get('name')
    instance = module.params.get('instance')
    volume_size = module.params.get('volume_size')
    encrypted = module.params.get('encrypted')
    kms_key_id = module.params.get('kms_key_id')
    device_name = module.params.get('device_name')
    zone = module.params.get('zone')
    snapshot = module.params.get('snapshot')
    state = module.params.get('state')
    tags = module.params.get('tags')
    if ((instance is None) and (zone is None) and (state == 'present')):
        module.fail_json(msg='You must specify either instance or zone')
    if ((instance == 'None') or (instance == '')):
        instance = None
        detach_vol_flag = True
    else:
        detach_vol_flag = False
    changed = False
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if region:
        try:
            ec2 = connect_to_aws(boto.ec2, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    else:
        module.fail_json(msg='region must be specified')
    if (state == 'list'):
        returned_volumes = []
        vols = get_volumes(module, ec2)
        for v in vols:
            attachment = v.attach_data
            returned_volumes.append(get_volume_info(v, state))
        module.exit_json(changed=False, volumes=returned_volumes)
    if (encrypted and (not boto_supports_volume_encryption())):
        module.fail_json(msg='You must use boto >= v2.29.0 to use encrypted volumes')
    if ((kms_key_id is not None) and (not boto_supports_kms_key_id())):
        module.fail_json(msg='You must use boto >= v2.39.0 to use kms_key_id')
    inst = None
    if instance:
        try:
            reservation = ec2.get_all_instances(instance_ids=instance)
        except BotoServerError as e:
            module.fail_json(msg=e.message)
        inst = reservation[0].instances[0]
        zone = inst.placement
        if device_name:
            if (device_name in inst.block_device_mapping):
                module.exit_json(msg=('Volume mapping for %s already exists on instance %s' % (device_name, instance)), volume_id=inst.block_device_mapping[device_name].volume_id, device=device_name, changed=False)
    if ((not volume_size) and (not (id or name or snapshot))):
        module.fail_json(msg='You must specify volume_size or identify an existing volume by id, name, or snapshot')
    if (volume_size and (id or snapshot)):
        module.fail_json(msg='Cannot specify volume_size together with id or snapshot')
    if (state == 'present'):
        (volume, changed) = create_volume(module, ec2, zone)
        if detach_vol_flag:
            (volume, changed) = detach_volume(module, ec2, volume)
        elif (inst is not None):
            (volume, changed) = attach_volume(module, ec2, volume, inst)
        volume_info = get_volume_info(volume, state)
        module.exit_json(changed=changed, volume=volume_info, device=volume_info['attachment_set']['device'], volume_id=volume_info['id'], volume_type=volume_info['type'])
    elif (state == 'absent'):
        delete_volume(module, ec2)
