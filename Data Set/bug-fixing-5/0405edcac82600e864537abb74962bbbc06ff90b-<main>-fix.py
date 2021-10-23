def main():
    '\n     Module action handler\n    '
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(id=dict(), name=dict(), tags=dict(type='dict', default={
        
    }), targets=dict(type='list', default=[])))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    (region, _, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = EFSConnection(module, region, **aws_connect_params)
    name = module.params.get('name')
    fs_id = module.params.get('id')
    tags = module.params.get('tags')
    targets = module.params.get('targets')
    file_systems_info = connection.get_file_systems(fs_id, name)
    if tags:
        file_systems_info = [item for item in file_systems_info if has_tags(item['tags'], tags)]
    if targets:
        targets = [(item, prefix_to_attr(item)) for item in targets]
        file_systems_info = [item for item in file_systems_info if has_targets(item['mount_targets'], targets)]
    module.exit_json(changed=False, ansible_facts={
        'efs': file_systems_info,
    })