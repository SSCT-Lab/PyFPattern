def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), state=dict(type='str', required=True, choices=['absent', 'present']), origin=dict(type='str', default=None), createparent=dict(type='bool', default=None), extra_zfs_properties=dict(type='dict', default={
        
    })), supports_check_mode=True, check_invalid_arguments=False)
    state = module.params.get('state')
    name = module.params.get('name')
    if (module.params.get('origin') and ('@' in name)):
        module.fail_json(msg='cannot specify origin when operating on a snapshot')
    properties = dict()
    for (prop, value) in module.params.items():
        if (prop not in module.argument_spec):
            if isinstance(value, bool):
                if (value is True):
                    properties[prop] = 'on'
                else:
                    properties[prop] = 'off'
            else:
                properties[prop] = value
    if properties:
        module.deprecate('Passing zfs properties as arbitrary parameters to the zfs module is deprecated.  Send them as a dictionary in the extra_zfs_properties parameter instead.', version='2.9')
        for (prop, value) in module.params['extra_zfs_properties'].items():
            properties[prop] = value
        module.params['extra_zfs_properties'] = properties
    for (prop, value) in module.params['extra_zfs_properties'].items():
        if isinstance(value, bool):
            if (value is True):
                module.params['extra_zfs_properties'][prop] = 'on'
            else:
                module.params['extra_zfs_properties'][prop] = 'off'
        else:
            module.params['extra_zfs_properties'][prop] = value
    result = dict(name=name, state=state)
    zfs = Zfs(module, name, module.params['extra_zfs_properties'])
    if (state == 'present'):
        if zfs.exists():
            zfs.set_properties_if_changed()
        else:
            zfs.create()
    elif (state == 'absent'):
        if zfs.exists():
            zfs.destroy()
    result.update(zfs.properties)
    result['changed'] = zfs.changed
    module.exit_json(**result)