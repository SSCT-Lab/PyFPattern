

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', aliases=['service', 'unit']), state=dict(type='str', choices=['reloaded', 'restarted', 'started', 'stopped']), enabled=dict(type='bool'), force=dict(type='bool'), masked=dict(type='bool'), daemon_reload=dict(type='bool', default=False, aliases=['daemon-reload']), daemon_reexec=dict(type='bool', default=False, aliases=['daemon-reexec']), user=dict(type='bool'), scope=dict(type='str', choices=['system', 'user', 'global']), no_block=dict(type='bool', default=False)), supports_check_mode=True, required_one_of=[['state', 'enabled', 'masked', 'daemon_reload', 'daemon_reexec']], required_by=dict(state=('name',), enabled=('name',), masked=('name',)), mutually_exclusive=[['scope', 'user']])
    systemctl = module.get_bin_path('systemctl', True)
    if (os.getenv('XDG_RUNTIME_DIR') is None):
        os.environ['XDG_RUNTIME_DIR'] = ('/run/user/%s' % os.geteuid())
    ' Set CLI options depending on params '
    if (module.params['user'] is not None):
        module.deprecate("The 'user' option is being replaced by 'scope'", version='2.11')
        if module.params['user']:
            module.params['scope'] = 'user'
        else:
            module.params['scope'] = 'system'
    if (module.params['scope'] not in (None, 'system')):
        systemctl += (' --%s' % module.params['scope'])
    if module.params['no_block']:
        systemctl += ' --no-block'
    if module.params['force']:
        systemctl += ' --force'
    unit = module.params['name']
    rc = 0
    out = err = ''
    result = dict(name=unit, changed=False, status=dict())
    if (module.params['daemon_reload'] and (not module.check_mode)):
        (rc, out, err) = module.run_command(('%s daemon-reload' % systemctl))
        if (rc != 0):
            module.fail_json(msg=('failure %d during daemon-reload: %s' % (rc, err)))
    if (module.params['daemon_reexec'] and (not module.check_mode)):
        (rc, out, err) = module.run_command(('%s daemon-reexec' % systemctl))
        if (rc != 0):
            module.fail_json(msg=('failure %d during daemon-reexec: %s' % (rc, err)))
    if unit:
        found = False
        is_initd = sysv_exists(unit)
        is_systemd = False
        (rc, out, err) = module.run_command(("%s show '%s'" % (systemctl, unit)))
        if (request_was_ignored(out) or request_was_ignored(err)):
            (rc, out, err) = module.run_command(("%s list-unit-files '%s'" % (systemctl, unit)))
            if (rc == 0):
                is_systemd = True
        elif (rc == 0):
            if out:
                result['status'] = parse_systemctl_show(to_native(out).split('\n'))
                is_systemd = (('LoadState' in result['status']) and (result['status']['LoadState'] != 'not-found'))
                is_masked = (('LoadState' in result['status']) and (result['status']['LoadState'] == 'masked'))
                if (is_systemd and (not is_masked) and ('LoadError' in result['status'])):
                    module.fail_json(msg=("Error loading unit file '%s': %s" % (unit, result['status']['LoadError'])))
        else:
            module.run_command(systemctl, check_rc=True)
        found = (is_systemd or is_initd)
        if (is_initd and (not is_systemd)):
            module.warn(('The service (%s) is actually an init script but the system is managed by systemd' % unit))
        if (module.params['masked'] is not None):
            masked = (('LoadState' in result['status']) and (result['status']['LoadState'] == 'masked'))
            if (masked != module.params['masked']):
                result['changed'] = True
                if module.params['masked']:
                    action = 'mask'
                else:
                    action = 'unmask'
                if (not module.check_mode):
                    (rc, out, err) = module.run_command(("%s %s '%s'" % (systemctl, action, unit)))
                    if (rc != 0):
                        fail_if_missing(module, found, unit, msg='host')
        if (module.params['enabled'] is not None):
            if module.params['enabled']:
                action = 'enable'
            else:
                action = 'disable'
            fail_if_missing(module, found, unit, msg='host')
            enabled = False
            (rc, out, err) = module.run_command(("%s is-enabled '%s'" % (systemctl, unit)))
            if (rc == 0):
                enabled = True
            elif (rc == 1):
                if ((module.params['scope'] in (None, 'system')) and (not module.params['user']) and is_initd and (not out.strip().endswith('disabled')) and sysv_is_enabled(unit)):
                    enabled = True
            result['enabled'] = enabled
            if (enabled != module.params['enabled']):
                result['changed'] = True
                if (not module.check_mode):
                    (rc, out, err) = module.run_command(("%s %s '%s'" % (systemctl, action, unit)))
                    if (rc != 0):
                        module.fail_json(msg=('Unable to %s service %s: %s' % (action, unit, (out + err))))
                result['enabled'] = (not enabled)
        if (module.params['state'] is not None):
            fail_if_missing(module, found, unit, msg='host')
            result['state'] = module.params['state']
            if ('ActiveState' in result['status']):
                action = None
                if (module.params['state'] == 'started'):
                    if (not is_running_service(result['status'])):
                        action = 'start'
                elif (module.params['state'] == 'stopped'):
                    if is_running_service(result['status']):
                        action = 'stop'
                else:
                    if (not is_running_service(result['status'])):
                        action = 'start'
                    else:
                        action = module.params['state'][:(- 2)]
                    result['state'] = 'started'
                if action:
                    result['changed'] = True
                    if (not module.check_mode):
                        (rc, out, err) = module.run_command(("%s %s '%s'" % (systemctl, action, unit)))
                        if (rc != 0):
                            module.fail_json(msg=('Unable to %s service %s: %s' % (action, unit, err)))
            elif is_chroot():
                module.warn('Target is a chroot. This can lead to false positives or prevent the init system tools from working.')
            else:
                module.fail_json(msg='Service is in unknown state', status=result['status'])
    module.exit_json(**result)
