def main():
    '\n     Module action handler\n    '
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(id=dict(), name=dict(), tags=dict(type='dict', default={
        
    }), targets=dict(type='list', default=[])))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, _, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = EFSConnection(module, region, **aws_connect_params)
    name = module.params.get('name')
    fs_id = module.params.get('id')
    tags = module.params.get('tags')
    targets = module.params.get('targets')
    file_systems_info = connection.get_file_systems(FileSystemId=fs_id, CreationToken=name)
    if tags:
        file_systems_info = filter((lambda item: has_tags(item['Tags'], tags)), file_systems_info)
    if targets:
        targets = [(item, prefix_to_attr(item)) for item in targets]
        file_systems_info = filter((lambda item: has_targets(item['MountTargets'], targets)), file_systems_info)
    file_systems_info = [camel_dict_to_snake_dict(x) for x in file_systems_info]
    module.exit_json(changed=False, ansible_facts={
        'efs': file_systems_info,
    })