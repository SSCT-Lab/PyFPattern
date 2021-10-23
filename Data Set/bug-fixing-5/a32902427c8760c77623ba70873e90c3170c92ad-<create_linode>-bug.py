def create_linode(module, client, **kwargs):
    'Creates a Linode instance and handles return format.'
    if (kwargs['root_pass'] is None):
        kwargs.pop('root_pass')
    try:
        response = client.linode.instance_create(**kwargs)
    except Exception as exception:
        raise module.fail_json(msg=('Unable to query the Linode API. Saw: %s' % exception))
    try:
        if isinstance(response, tuple):
            (instance, root_pass) = response
            instance_json = instance._raw_json
            instance_json.update({
                'root_pass': root_pass,
            })
            return instance_json
        else:
            return response._raw_json
    except TypeError:
        raise module.fail_json(msg='Unable to parse Linode instance creation response. Please raise a bug against this module on https://github.com/ansible/ansible/issues')