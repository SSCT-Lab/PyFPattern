def get_instance_info(instance):
    groups = []
    for group in instance.groups:
        groups.append({
            'id': group.id,
            'name': group.name,
        }.copy())
    interfaces = []
    for interface in instance.interfaces:
        interfaces.append({
            'id': interface.id,
            'mac_address': interface.mac_address,
        }.copy())
    try:
        source_dest_check = instance.sourceDestCheck
    except AttributeError:
        source_dest_check = None
    try:
        bdm_dict = []
        bdm = getattr(instance, 'block_device_mapping')
        for device_name in bdm.keys():
            bdm_dict.append({
                'device_name': device_name,
                'status': bdm[device_name].status,
                'volume_id': bdm[device_name].volume_id,
                'delete_on_termination': bdm[device_name].delete_on_termination,
                'attach_time': bdm[device_name].attach_time,
            })
    except AttributeError:
        pass
    instance_profile = (dict(instance.instance_profile) if (instance.instance_profile is not None) else None)
    instance_info = {
        'id': instance.id,
        'kernel': instance.kernel,
        'instance_profile': instance_profile,
        'root_device_type': instance.root_device_type,
        'private_dns_name': instance.private_dns_name,
        'public_dns_name': instance.public_dns_name,
        'ebs_optimized': instance.ebs_optimized,
        'client_token': instance.client_token,
        'virtualization_type': instance.virtualization_type,
        'architecture': instance.architecture,
        'ramdisk': instance.ramdisk,
        'tags': instance.tags,
        'key_name': instance.key_name,
        'source_destination_check': source_dest_check,
        'image_id': instance.image_id,
        'groups': groups,
        'interfaces': interfaces,
        'spot_instance_request_id': instance.spot_instance_request_id,
        'requester_id': instance.requester_id,
        'monitoring_state': instance.monitoring_state,
        'placement': {
            'tenancy': instance._placement.tenancy,
            'zone': instance._placement.zone,
        },
        'ami_launch_index': instance.ami_launch_index,
        'launch_time': instance.launch_time,
        'hypervisor': instance.hypervisor,
        'region': instance.region.name,
        'persistent': instance.persistent,
        'private_ip_address': instance.private_ip_address,
        'public_ip_address': instance.ip_address,
        'state': instance._state.name,
        'vpc_id': instance.vpc_id,
        'block_device_mapping': bdm_dict,
    }
    return instance_info