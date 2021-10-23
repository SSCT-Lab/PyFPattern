

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), state=dict(type='str', choices=['killed', 'once', 'reloaded', 'restarted', 'started', 'stopped']), enabled=dict(type='bool'), downed=dict(type='bool'), dist=dict(type='str', default='daemontools'), service_dir=dict(type='str', default='/service'), service_src=dict(type='str', default='/etc/service')), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    state = module.params['state']
    enabled = module.params['enabled']
    downed = module.params['downed']
    svc = Svc(module)
    changed = False
    orig_state = svc.report()
    if ((enabled is not None) and (enabled != svc.enabled)):
        changed = True
        if (not module.check_mode):
            try:
                if enabled:
                    svc.enable()
                else:
                    svc.disable()
            except (OSError, IOError) as e:
                module.fail_json(msg=('Could change service link: %s' % to_native(e)))
    if ((state is not None) and (state != svc.state)):
        changed = True
        if (not module.check_mode):
            getattr(svc, state[:(- 2)])()
    if ((downed is not None) and (downed != svc.downed)):
        changed = True
        if (not module.check_mode):
            d_file = ('%s/down' % svc.svc_full)
            try:
                if downed:
                    open(d_file, 'a').close()
                else:
                    os.unlink(d_file)
            except (OSError, IOError) as e:
                module.fail_json(msg=('Could change downed file: %s ' % to_native(e)))
    module.exit_json(changed=changed, svc=svc.report())
