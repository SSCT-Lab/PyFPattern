def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(owner=dict(required=False, default=None), ami_id=dict(required=False), ami_tags=dict(required=False, type='dict', aliases=['search_tags', 'image_tags']), architecture=dict(required=False), hypervisor=dict(required=False), is_public=dict(required=False, type='bool'), name=dict(required=False), platform=dict(required=False), sort=dict(required=False, default=None, choices=['name', 'description', 'tag', 'architecture', 'block_device_mapping', 'creationDate', 'hypervisor', 'is_public', 'location', 'owner_id', 'platform', 'root_device_name', 'root_device_type', 'state', 'virtualization_type']), sort_tag=dict(required=False), sort_order=dict(required=False, default='ascending', choices=['ascending', 'descending']), sort_start=dict(required=False), sort_end=dict(required=False), state=dict(required=False, default='available'), virtualization_type=dict(required=False), no_result_action=dict(required=False, default='success', choices=['success', 'fail'])))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module, install via pip or your package manager')
    ami_id = module.params.get('ami_id')
    ami_tags = module.params.get('ami_tags')
    architecture = module.params.get('architecture')
    hypervisor = module.params.get('hypervisor')
    is_public = module.params.get('is_public')
    name = module.params.get('name')
    owner = module.params.get('owner')
    platform = module.params.get('platform')
    sort = module.params.get('sort')
    sort_tag = module.params.get('sort_tag')
    sort_order = module.params.get('sort_order')
    sort_start = module.params.get('sort_start')
    sort_end = module.params.get('sort_end')
    state = module.params.get('state')
    virtualization_type = module.params.get('virtualization_type')
    no_result_action = module.params.get('no_result_action')
    filter = {
        'state': state,
    }
    if ami_id:
        filter['image_id'] = ami_id
    if ami_tags:
        for tag in ami_tags:
            filter[('tag:' + tag)] = ami_tags[tag]
    if architecture:
        filter['architecture'] = architecture
    if hypervisor:
        filter['hypervisor'] = hypervisor
    if is_public:
        filter['is_public'] = 'true'
    if name:
        filter['name'] = name
    if platform:
        filter['platform'] = platform
    if virtualization_type:
        filter['virtualization_type'] = virtualization_type
    ec2 = ec2_connect(module)
    images_result = ec2.get_all_images(owners=owner, filters=filter)
    if ((no_result_action == 'fail') and (len(images_result) == 0)):
        module.fail_json(msg=('No AMIs matched the attributes: %s' % json.dumps(filter)))
    results = []
    for image in images_result:
        data = {
            'ami_id': image.id,
            'architecture': image.architecture,
            'block_device_mapping': get_block_device_mapping(image),
            'creationDate': image.creationDate,
            'description': image.description,
            'hypervisor': image.hypervisor,
            'is_public': image.is_public,
            'location': image.location,
            'name': image.name,
            'owner_id': image.owner_id,
            'platform': image.platform,
            'root_device_name': image.root_device_name,
            'root_device_type': image.root_device_type,
            'state': image.state,
            'tags': image.tags,
            'virtualization_type': image.virtualization_type,
        }
        if image.kernel_id:
            data['kernel_id'] = image.kernel_id
        if image.ramdisk_id:
            data['ramdisk_id'] = image.ramdisk_id
        results.append(data)
    if (sort == 'tag'):
        if (not sort_tag):
            module.fail_json(msg="'sort_tag' option must be given with 'sort=tag'")
        results.sort(key=(lambda e: e['tags'][sort_tag]), reverse=(sort_order == 'descending'))
    elif sort:
        results.sort(key=(lambda e: e[sort]), reverse=(sort_order == 'descending'))
    try:
        if (sort and sort_start and sort_end):
            results = results[int(sort_start):int(sort_end)]
        elif (sort and sort_start):
            results = results[int(sort_start):]
        elif (sort and sort_end):
            results = results[:int(sort_end)]
    except TypeError:
        module.fail_json(msg='Please supply numeric values for sort_start and/or sort_end')
    module.exit_json(results=results)