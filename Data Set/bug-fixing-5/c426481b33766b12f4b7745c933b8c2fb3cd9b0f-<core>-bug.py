def core(module):
    state = module.params.get('state', None)
    autostart = module.params.get('autostart', None)
    guest = module.params.get('name', None)
    command = module.params.get('command', None)
    uri = module.params.get('uri', None)
    xml = module.params.get('xml', None)
    v = Virt(uri, module)
    res = {
        
    }
    if (state and (command == 'list_vms')):
        res = v.list_vms(state=state)
        if (not isinstance(res, dict)):
            res = {
                command: res,
            }
        return (VIRT_SUCCESS, res)
    if state:
        if (not guest):
            module.fail_json(msg='state change requires a guest specified')
        if (state == 'running'):
            if (v.status(guest) is 'paused'):
                res['changed'] = True
                res['msg'] = v.unpause(guest)
            elif (v.status(guest) is not 'running'):
                res['changed'] = True
                res['msg'] = v.start(guest)
        elif (state == 'shutdown'):
            if (v.status(guest) is not 'shutdown'):
                res['changed'] = True
                res['msg'] = v.shutdown(guest)
        elif (state == 'destroyed'):
            if (v.status(guest) is not 'shutdown'):
                res['changed'] = True
                res['msg'] = v.destroy(guest)
        elif (state == 'paused'):
            if (v.status(guest) is 'running'):
                res['changed'] = True
                res['msg'] = v.pause(guest)
        else:
            module.fail_json(msg='unexpected state')
        return (VIRT_SUCCESS, res)
    if ((autostart is not None) and v.autostart(guest, autostart)):
        res['changed'] = True
    if command:
        if (command in VM_COMMANDS):
            if (not guest):
                module.fail_json(msg=('%s requires 1 argument: guest' % command))
            if (command == 'define'):
                if (not xml):
                    module.fail_json(msg='define requires xml argument')
                try:
                    v.get_vm(guest)
                except VMNotFound:
                    v.define(xml)
                    res = {
                        'changed': True,
                        'created': guest,
                    }
                return (VIRT_SUCCESS, res)
            res = getattr(v, command)(guest)
            if (not isinstance(res, dict)):
                res = {
                    command: res,
                }
            return (VIRT_SUCCESS, res)
        elif hasattr(v, command):
            res = getattr(v, command)()
            if (not isinstance(res, dict)):
                res = {
                    command: res,
                }
            return (VIRT_SUCCESS, res)
        else:
            module.fail_json(msg=('Command %s not recognized' % basecmd))
    module.fail_json(msg='expected state or command parameter to be specified')