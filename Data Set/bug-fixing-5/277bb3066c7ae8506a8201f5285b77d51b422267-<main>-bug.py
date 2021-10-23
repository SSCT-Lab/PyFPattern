def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), persistent=dict(type='bool', default=False), state=dict(type='bool', required=True)), supports_check_mode=True)
    if (not HAVE_SELINUX):
        module.fail_json(msg='This module requires libselinux-python support')
    if (not HAVE_SEMANAGE):
        module.fail_json(msg='This module requires libsemanage-python support')
    if (not selinux.is_selinux_enabled()):
        module.fail_json(msg='SELinux is disabled on this host.')
    name = module.params['name']
    persistent = module.params['persistent']
    state = module.params['state']
    result = dict(name=name)
    if hasattr(selinux, 'selinux_boolean_sub'):
        name = selinux.selinux_boolean_sub(name)
    if (not has_boolean_value(module, name)):
        module.fail_json(msg=('SELinux boolean %s does not exist.' % name))
    cur_value = get_boolean_value(module, name)
    if (cur_value == state):
        module.exit_json(changed=False, state=cur_value, **result)
    if module.check_mode:
        module.exit_json(changed=True)
    if persistent:
        r = semanage_boolean_value(module, name, state)
    else:
        r = set_boolean_value(module, name, state)
    result['changed'] = r
    if (not r):
        module.fail_json(msg=('Failed to set boolean %s to %s' % (name, state)))
    try:
        selinux.security_commit_booleans()
    except:
        module.fail_json(msg=('Failed to commit pending boolean %s value' % name))
    module.exit_json(**result)