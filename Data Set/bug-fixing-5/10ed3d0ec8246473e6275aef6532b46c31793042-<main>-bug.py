def main():
    fields = {
        'api_url': {
            'required': False,
            'type': 'str',
        },
        'api_username': {
            'required': False,
            'type': 'str',
        },
        'api_password': {
            'required': False,
            'type': 'str',
            'no_log': True,
        },
        'ids': {
            'required': False,
            'aliases': ['id'],
            'type': 'list',
        },
        'name': {
            'required': False,
            'type': 'str',
        },
    }
    module = AnsibleModule(argument_spec=fields, mutually_exclusive=[['ids', 'name']], supports_check_mode=True)
    if (module._name == 'one_image_facts'):
        module.deprecate("The 'one_image_facts' module has been renamed to 'one_image_info'", version='2.13')
    if (not HAS_OCA):
        module.fail_json(msg='This module requires python-oca to work!')
    auth = get_connection_info(module)
    params = module.params
    ids = params.get('ids')
    name = params.get('name')
    client = oca.Client(((auth.username + ':') + auth.password), auth.url)
    result = {
        'images': [],
    }
    images = []
    if ids:
        images = get_images_by_ids(module, client, ids)
    elif name:
        images = get_images_by_name(module, client, name)
    else:
        images = get_all_images(client)
    for image in images:
        result['images'].append(get_image_info(image))
    module.exit_json(**result)