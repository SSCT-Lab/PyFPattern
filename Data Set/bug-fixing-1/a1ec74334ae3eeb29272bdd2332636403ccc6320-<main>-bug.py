

def main():
    argument_spec = cloudscale_argument_spec()
    argument_spec.update(dict(state=dict(default='present', choices=('present', 'absent')), name=dict(), uuid=dict(), size_gb=dict(type='int'), type=dict(choices=('ssd', 'bulk')), server_uuids=dict(type='list', aliases=['server_uuid'])))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=(('name', 'uuid'),), mutually_exclusive=(('name', 'uuid'),), supports_check_mode=True)
    volume = AnsibleCloudscaleVolume(module)
    if module.check_mode:
        changed = False
        for (param, conv) in (('state', str), ('server_uuids', set), ('size_gb', int)):
            if (module.params[param] is None):
                continue
            if (conv(volume.info[param]) != conv(module.params[param])):
                changed = True
                break
        module.exit_json(changed=changed, **volume.info)
    if ((volume.info['state'] == 'absent') and (module.params['state'] == 'present')):
        volume.create()
    elif ((volume.info['state'] == 'present') and (module.params['state'] == 'absent')):
        volume.delete()
    if (module.params['state'] == 'present'):
        for (param, conv) in (('server_uuids', set), ('size_gb', int)):
            if (module.params[param] is None):
                continue
            if (conv(volume.info[param]) != conv(module.params[param])):
                volume.update(param)
        if ((module.params['type'] is not None) and (volume.info['type'] != module.params['type'])):
            module.fail_json(msg='Cannot change type of an existing volume.')
    module.exit_json(changed=volume.changed, **volume.info)
