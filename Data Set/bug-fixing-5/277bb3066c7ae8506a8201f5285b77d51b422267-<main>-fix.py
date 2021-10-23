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
    result = dict(name=name, persistent=persistent, state=state)
    changed = False
    if hasattr(selinux, 'selinux_boolean_sub'):
        name = selinux.selinux_boolean_sub(name)
    if (not has_boolean_value(module, name)):
        module.fail_json(msg=('SELinux boolean %s does not exist.' % name))
    if persistent:
        changed = semanage_boolean_value(module, name, state)
    else:
        cur_value = get_boolean_value(module, name)
        if (cur_value != state):
            changed = True
            if (not module.check_mode):
                changed = set_boolean_value(module, name, state)
                if (not changed):
                    module.fail_json(msg=('Failed to set boolean %s to %s' % (name, state)))
                try:
                    selinux.security_commit_booleans()
                except:
                    module.fail_json(msg=('Failed to commit pending boolean %s value' % name))
    result['changed'] = changed
    module.exit_json(**result)