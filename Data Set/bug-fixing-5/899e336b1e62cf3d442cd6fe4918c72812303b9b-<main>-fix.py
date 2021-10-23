def main():
    module = AnsibleModule(argument_spec=dict(force=dict(default=None, type='bool'), pool=dict(default='zones'), source=dict(default=None), state=dict(default=None, required=True, choices=['present', 'absent', 'deleted', 'imported', 'updated', 'vacuumed']), type=dict(default='imgapi', choices=['imgapi', 'docker', 'dsapi']), uuid=dict(default=None)), supports_check_mode=False)
    imgadm = Imgadm(module)
    uuid = module.params['uuid']
    source = module.params['source']
    state = module.params['state']
    result = {
        'state': state,
    }
    if source:
        result['source'] = source
        imgadm.manage_sources()
    else:
        result['uuid'] = uuid
        if (state == 'updated'):
            imgadm.update_images()
        else:
            if ((uuid == '*') and (state != 'vacuumed')):
                module.fail_json(msg='Can only specify uuid as "*" when updating image(s)')
            imgadm.manage_images()
    result['changed'] = imgadm.changed
    module.exit_json(**result)