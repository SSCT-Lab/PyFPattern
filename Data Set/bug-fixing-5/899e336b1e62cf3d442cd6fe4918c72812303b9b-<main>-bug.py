def main():
    module = AnsibleModule(argument_spec=dict(force=dict(default=None, type='bool'), pool=dict(default='zones'), source=dict(default=None), state=dict(default=None, required=True, choices=['present', 'absent', 'deleted', 'imported', 'updated', 'vacuumed']), type=dict(default='imgapi', choices=['imgapi', 'docker', 'dsapi']), uuid=dict(default=None)), supports_check_mode=False)
    uuid = module.params['uuid']
    source = module.params['source']
    state = module.params['state']
    if (state in ['present', 'imported', 'updated']):
        present = True
    else:
        present = False
    stderr = stdout = ''
    rc = 0
    result = {
        'state': state,
    }
    changed = False
    if (uuid and (uuid != '*')):
        if (not re.match('^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$', uuid, re.IGNORECASE)):
            module.fail_json(msg='Provided value for uuid option is not a valid UUID.')
    if module.params['source']:
        (rc, stdout, stderr, changed) = manage_sources(module, present)
        result['source'] = source
    else:
        result['uuid'] = uuid
        if (state == 'updated'):
            (rc, stdout, stderr, changed) = update_images(module)
        else:
            if ((uuid == '*') and (state != 'vacuumed')):
                module.fail_json(msg='Can only specify uuid as "*" when updating image(s)')
            (rc, stdout, stderr, changed) = manage_images(module, present)
    if (rc != 0):
        if stderr:
            module.fail_json(msg=stderr)
        else:
            module.fail_json(msg=stdout)
    result['changed'] = changed
    module.exit_json(**result)