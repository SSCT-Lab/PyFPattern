def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(key_name=dict(aliases=['keypair']), id=dict(), group=dict(type='list', aliases=['groups']), group_id=dict(type='list'), zone=dict(aliases=['aws_zone', 'ec2_zone']), instance_type=dict(aliases=['type']), spot_price=dict(), spot_type=dict(default='one-time', choices=['one-time', 'persistent']), spot_launch_group=dict(), image=dict(), kernel=dict(), count=dict(type='int', default='1'), monitoring=dict(type='bool', default=False), ramdisk=dict(), wait=dict(type='bool', default=False), wait_timeout=dict(default=300), spot_wait_timeout=dict(default=600), placement_group=dict(), user_data=dict(), instance_tags=dict(type='dict'), vpc_subnet_id=dict(), assign_public_ip=dict(type='bool'), private_ip=dict(), instance_profile_name=dict(), instance_ids=dict(type='list', aliases=['instance_id']), source_dest_check=dict(type='bool', default=None), termination_protection=dict(type='bool', default=None), state=dict(default='present', choices=['present', 'absent', 'running', 'restarted', 'stopped']), instance_initiated_shutdown_behavior=dict(default='stop', choices=['stop', 'terminate']), exact_count=dict(type='int', default=None), count_tag=dict(), volumes=dict(type='list'), ebs_optimized=dict(type='bool', default=False), tenancy=dict(default='default', choices=['default', 'dedicated']), network_interfaces=dict(type='list', aliases=['network_interface'])))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['group_name', 'group_id'], ['exact_count', 'count'], ['exact_count', 'state'], ['exact_count', 'instance_ids'], ['network_interfaces', 'assign_public_ip'], ['network_interfaces', 'group'], ['network_interfaces', 'group_id'], ['network_interfaces', 'private_ip'], ['network_interfaces', 'vpc_subnet_id']])
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
        if (module.params.get('region') or (not module.params.get('ec2_url'))):
            ec2 = ec2_connect(module)
        elif module.params.get('ec2_url'):
            ec2 = connect_ec2_endpoint(ec2_url, **aws_connect_kwargs)
        if ('region' not in aws_connect_kwargs):
            aws_connect_kwargs['region'] = ec2.region
        vpc = connect_vpc(**aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=('Failed to get connection: %s' % e.message), exception=traceback.format_exc())
    tagged_instances = []
    state = module.params['state']
    if (state == 'absent'):
        instance_ids = module.params['instance_ids']
        if (not instance_ids):
            module.fail_json(msg='instance_ids list is required for absent state')
        (changed, instance_dict_array, new_instance_ids) = terminate_instances(module, ec2, instance_ids)
    elif (state in ('running', 'stopped')):
        instance_ids = module.params.get('instance_ids')
        instance_tags = module.params.get('instance_tags')
        if (not (isinstance(instance_ids, list) or isinstance(instance_tags, dict))):
            module.fail_json(msg=('running list needs to be a list of instances or set of tags to run: %s' % instance_ids))
        (changed, instance_dict_array, new_instance_ids) = startstop_instances(module, ec2, instance_ids, state, instance_tags)
    elif (state in 'restarted'):
        instance_ids = module.params.get('instance_ids')
        instance_tags = module.params.get('instance_tags')
        if (not (isinstance(instance_ids, list) or isinstance(instance_tags, dict))):
            module.fail_json(msg=('running list needs to be a list of instances or set of tags to run: %s' % instance_ids))
        (changed, instance_dict_array, new_instance_ids) = restart_instances(module, ec2, instance_ids, state, instance_tags)
    elif (state == 'present'):
        if (not module.params.get('image')):
            module.fail_json(msg='image parameter is required for new instance')
        if (module.params.get('exact_count') is None):
            (instance_dict_array, new_instance_ids, changed) = create_instances(module, ec2, vpc)
        else:
            (tagged_instances, instance_dict_array, new_instance_ids, changed) = enforce_count(module, ec2, vpc)
    if new_instance_ids:
        new_instance_ids.sort()
    if instance_dict_array:
        instance_dict_array.sort(key=(lambda x: x['id']))
    if tagged_instances:
        tagged_instances.sort(key=(lambda x: x['id']))
    module.exit_json(changed=changed, instance_ids=new_instance_ids, instances=instance_dict_array, tagged_instances=tagged_instances)