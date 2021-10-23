

def build_top_level_options(params):
    spec = {
        
    }
    if params.get('image_id'):
        spec['ImageId'] = params['image_id']
    elif isinstance(params.get('image'), dict):
        image = params.get('image', {
            
        })
        spec['ImageId'] = image.get('id')
        if ('ramdisk' in image):
            spec['RamdiskId'] = image['ramdisk']
        if ('kernel' in image):
            spec['KernelId'] = image['kernel']
    if ((not spec.get('ImageId')) and (not params.get('launch_template'))):
        module.fail_json(msg='You must include an image_id or image.id parameter to create an instance, or use a launch_template.')
    if (params.get('key_name') is not None):
        spec['KeyName'] = params.get('key_name')
    if (params.get('user_data') is not None):
        spec['UserData'] = to_native(params.get('user_data'))
    elif (params.get('tower_callback') is not None):
        spec['UserData'] = tower_callback_script(tower_conf=params.get('tower_callback'), windows=params.get('tower_callback').get('windows', False), passwd=params.get('tower_callback').get('set_password'))
    if (params.get('launch_template') is not None):
        spec['LaunchTemplate'] = {
            
        }
        if ((not params.get('launch_template').get('id')) or params.get('launch_template').get('name')):
            module.fail_json(msg='Could not create instance with launch template. Either launch_template.name or launch_template.id parameters are required')
        if (params.get('launch_template').get('id') is not None):
            spec['LaunchTemplate']['LaunchTemplateId'] = params.get('launch_template').get('id')
        if (params.get('launch_template').get('name') is not None):
            spec['LaunchTemplate']['LaunchTemplateName'] = params.get('launch_template').get('name')
        if (params.get('launch_template').get('version') is not None):
            spec['LaunchTemplate']['Version'] = to_native(params.get('launch_template').get('version'))
    if params.get('detailed_monitoring', False):
        spec['Monitoring'] = {
            'Enabled': True,
        }
    if (params.get('cpu_credit_specification') is not None):
        spec['CreditSpecification'] = {
            'CpuCredits': params.get('cpu_credit_specification'),
        }
    if (params.get('tenancy') is not None):
        spec['Placement'] = {
            'Tenancy': params.get('tenancy'),
        }
    if params.get('placement_group'):
        spec.setdefault('Placement', {
            'GroupName': str(params.get('placement_group')),
        })
    if (params.get('ebs_optimized') is not None):
        spec['EbsOptimized'] = params.get('ebs_optimized')
    if params.get('instance_initiated_shutdown_behavior'):
        spec['InstanceInitiatedShutdownBehavior'] = params.get('instance_initiated_shutdown_behavior')
    if (params.get('termination_protection') is not None):
        spec['DisableApiTermination'] = params.get('termination_protection')
    if (params.get('cpu_options') is not None):
        spec['CpuOptions'] = {
            
        }
        spec['CpuOptions']['ThreadsPerCore'] = params.get('cpu_options').get('threads_per_core')
        spec['CpuOptions']['CoreCount'] = params.get('cpu_options').get('core_count')
    return spec
