def create_instances(module, ec2, vpc, override_count=None):
    '\n    Creates new instances\n\n    module : AnsibleModule object\n    ec2: authenticated ec2 connection object\n\n    Returns:\n        A list of dictionaries with instance information\n        about the instances that were launched\n    '
    key_name = module.params.get('key_name')
    id = module.params.get('id')
    group_name = module.params.get('group')
    group_id = module.params.get('group_id')
    zone = module.params.get('zone')
    instance_type = module.params.get('instance_type')
    tenancy = module.params.get('tenancy')
    spot_price = module.params.get('spot_price')
    spot_type = module.params.get('spot_type')
    image = module.params.get('image')
    if override_count:
        count = override_count
    else:
        count = module.params.get('count')
    monitoring = module.params.get('monitoring')
    kernel = module.params.get('kernel')
    ramdisk = module.params.get('ramdisk')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    spot_wait_timeout = int(module.params.get('spot_wait_timeout'))
    placement_group = module.params.get('placement_group')
    user_data = module.params.get('user_data')
    instance_tags = module.params.get('instance_tags')
    vpc_subnet_id = module.params.get('vpc_subnet_id')
    assign_public_ip = module.boolean(module.params.get('assign_public_ip'))
    private_ip = module.params.get('private_ip')
    instance_profile_name = module.params.get('instance_profile_name')
    volumes = module.params.get('volumes')
    ebs_optimized = module.params.get('ebs_optimized')
    exact_count = module.params.get('exact_count')
    count_tag = module.params.get('count_tag')
    source_dest_check = module.boolean(module.params.get('source_dest_check'))
    termination_protection = module.boolean(module.params.get('termination_protection'))
    network_interfaces = module.params.get('network_interfaces')
    spot_launch_group = module.params.get('spot_launch_group')
    instance_initiated_shutdown_behavior = module.params.get('instance_initiated_shutdown_behavior')
    vpc_id = None
    if vpc_subnet_id:
        if (not vpc):
            module.fail_json(msg='region must be specified')
        else:
            vpc_id = vpc.get_all_subnets(subnet_ids=[vpc_subnet_id])[0].vpc_id
    else:
        vpc_id = None
    try:
        if group_name:
            if vpc_id:
                grp_details = ec2.get_all_security_groups(filters={
                    'vpc_id': vpc_id,
                })
            else:
                grp_details = ec2.get_all_security_groups()
            if isinstance(group_name, string_types):
                group_name = [group_name]
            unmatched = set(group_name).difference((str(grp.name) for grp in grp_details))
            if (len(unmatched) > 0):
                module.fail_json(msg=('The following group names are not valid: %s' % ', '.join(unmatched)))
            group_id = [str(grp.id) for grp in grp_details if (str(grp.name) in group_name)]
        elif group_id:
            if isinstance(group_id, string_types):
                group_id = [group_id]
            grp_details = ec2.get_all_security_groups(group_ids=group_id)
            group_name = [grp_item.name for grp_item in grp_details]
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    running_instances = []
    count_remaining = int(count)
    if (id is not None):
        filter_dict = {
            'client-token': id,
            'instance-state-name': 'running',
        }
        previous_reservations = ec2.get_all_instances(None, filter_dict)
        for res in previous_reservations:
            for prev_instance in res.instances:
                running_instances.append(prev_instance)
        count_remaining = (count_remaining - len(running_instances))
    if (count_remaining == 0):
        changed = False
    else:
        changed = True
        try:
            params = {
                'image_id': image,
                'key_name': key_name,
                'monitoring_enabled': monitoring,
                'placement': zone,
                'instance_type': instance_type,
                'kernel_id': kernel,
                'ramdisk_id': ramdisk,
                'user_data': user_data,
            }
            if ebs_optimized:
                params['ebs_optimized'] = ebs_optimized
            if (not spot_price):
                params['tenancy'] = tenancy
            if boto_supports_profile_name_arg(ec2):
                params['instance_profile_name'] = instance_profile_name
            elif (instance_profile_name is not None):
                module.fail_json(msg='instance_profile_name parameter requires Boto version 2.5.0 or higher')
            if assign_public_ip:
                if (not boto_supports_associate_public_ip_address(ec2)):
                    module.fail_json(msg='assign_public_ip parameter requires Boto version 2.13.0 or higher.')
                elif (not vpc_subnet_id):
                    module.fail_json(msg='assign_public_ip only available with vpc_subnet_id')
                else:
                    if private_ip:
                        interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=vpc_subnet_id, private_ip_address=private_ip, groups=group_id, associate_public_ip_address=assign_public_ip)
                    else:
                        interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=vpc_subnet_id, groups=group_id, associate_public_ip_address=assign_public_ip)
                    interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)
                    params['network_interfaces'] = interfaces
            elif network_interfaces:
                if isinstance(network_interfaces, string_types):
                    network_interfaces = [network_interfaces]
                interfaces = []
                for (i, network_interface_id) in enumerate(network_interfaces):
                    interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(network_interface_id=network_interface_id, device_index=i)
                    interfaces.append(interface)
                params['network_interfaces'] = boto.ec2.networkinterface.NetworkInterfaceCollection(*interfaces)
            else:
                params['subnet_id'] = vpc_subnet_id
                if vpc_subnet_id:
                    params['security_group_ids'] = group_id
                else:
                    params['security_groups'] = group_name
            if volumes:
                bdm = BlockDeviceMapping()
                for volume in volumes:
                    if ('device_name' not in volume):
                        module.fail_json(msg='Device name must be set for volume')
                    if (('volume_size' not in volume) or (int(volume['volume_size']) > 0)):
                        bdm[volume['device_name']] = create_block_device(module, ec2, volume)
                params['block_device_map'] = bdm
            if (not spot_price):
                if (assign_public_ip and private_ip):
                    params.update(dict(min_count=count_remaining, max_count=count_remaining, client_token=id, placement_group=placement_group))
                else:
                    params.update(dict(min_count=count_remaining, max_count=count_remaining, client_token=id, placement_group=placement_group, private_ip_address=private_ip))
                params['instance_initiated_shutdown_behavior'] = (instance_initiated_shutdown_behavior or 'stop')
                res = ec2.run_instances(**params)
                instids = [i.id for i in res.instances]
                while True:
                    try:
                        ec2.get_all_instances(instids)
                        break
                    except boto.exception.EC2ResponseError as e:
                        if ('<Code>InvalidInstanceID.NotFound</Code>' in str(e)):
                            continue
                        else:
                            module.fail_json(msg=str(e))
                terminated_instances = [str(instance.id) for instance in res.instances if (instance.state == 'terminated')]
                if terminated_instances:
                    module.fail_json(msg=((('Instances with id(s) %s ' % terminated_instances) + 'were created previously but have since been terminated - ') + "use a (possibly different) 'instanceid' parameter"))
            else:
                if private_ip:
                    module.fail_json(msg='private_ip only available with on-demand (non-spot) instances')
                if boto_supports_param_in_spot_request(ec2, 'placement_group'):
                    params['placement_group'] = placement_group
                elif placement_group:
                    module.fail_json(msg='placement_group parameter requires Boto version 2.3.0 or higher.')
                if (instance_initiated_shutdown_behavior and (instance_initiated_shutdown_behavior != 'terminate')):
                    module.fail_json(msg='instance_initiated_shutdown_behavior=stop is not supported for spot instances.')
                if (spot_launch_group and isinstance(spot_launch_group, string_types)):
                    params['launch_group'] = spot_launch_group
                params.update(dict(count=count_remaining, type=spot_type))
                res = ec2.request_spot_instances(spot_price, **params)
                if wait:
                    instids = await_spot_requests(module, ec2, res, count)
                else:
                    instids = []
        except boto.exception.BotoServerError as e:
            module.fail_json(msg=('Instance creation failed => %s: %s' % (e.error_code, e.error_message)))
        num_running = 0
        wait_timeout = (time.time() + wait_timeout)
        res_list = ()
        while ((wait_timeout > time.time()) and (num_running < len(instids))):
            try:
                res_list = ec2.get_all_instances(instids)
            except boto.exception.BotoServerError as e:
                if (e.error_code == 'InvalidInstanceID.NotFound'):
                    time.sleep(1)
                    continue
                else:
                    raise
            num_running = 0
            for res in res_list:
                num_running += len([i for i in res.instances if (i.state == 'running')])
            if (len(res_list) <= 0):
                time.sleep(1)
                continue
            if (wait and (num_running < len(instids))):
                time.sleep(5)
            else:
                break
        if (wait and (wait_timeout <= time.time())):
            module.fail_json(msg=('wait for instances running timeout on %s' % time.asctime()))
        for res in res_list:
            running_instances.extend(res.instances)
        if (source_dest_check is False):
            for inst in res.instances:
                inst.modify_attribute('sourceDestCheck', False)
        if (termination_protection is True):
            for inst in res.instances:
                inst.modify_attribute('disableApiTermination', True)
        if (instance_tags and instids):
            try:
                ec2.create_tags(instids, instance_tags)
            except boto.exception.EC2ResponseError as e:
                module.fail_json(msg=('Instance tagging failed => %s: %s' % (e.error_code, e.error_message)))
    instance_dict_array = []
    created_instance_ids = []
    for inst in running_instances:
        inst.update()
        d = get_instance_info(inst)
        created_instance_ids.append(inst.id)
        instance_dict_array.append(d)
    return (instance_dict_array, created_instance_ids, changed)