def core(module):
    state = module.params.get('state', None)
    autostart = module.params.get('autostart', None)
    guest = module.params.get('name', None)
    command = module.params.get('command', None)
    uri = module.params.get('uri', None)
    xml = module.params.get('xml', None)
    v = Virt(uri, module)
    res = dict()
    if (state and (command == 'list_vms')):
        res = v.list_vms(state=state)
        if (not isinstance(res, dict)):
            res = {
                command: res,
            }
        return (VIRT_SUCCESS, res)
    if ((autostart is not None) and (command != 'define')):
        if (not guest):
            module.fail_json(msg='autostart requires 1 argument: name')
        try:
            v.get_vm(guest)
        except VMNotFound:
            module.fail_json(msg=('domain %s not found' % guest))
        res['changed'] = v.autostart(guest, autostart)
        if ((not command) and (not state)):
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
    if command:
        if (command in VM_COMMANDS):
            if (command == 'define'):
                if (not xml):
                    module.fail_json(msg='define requires xml argument')
                if guest:
                    module.warn("'xml' is given - ignoring 'name'")
                found_name = re.search('<name>(.*)</name>', xml).groups()
                if found_name:
                    domain_name = found_name[0]
                else:
                    module.fail_json(msg="Could not find domain 'name' in xml")
                try:
                    existing_domain = v.get_vm(domain_name)
                except VMNotFound:
                    existing_domain = None
                try:
                    domain = v.define(xml)
                    if existing_domain:
                        if (existing_domain.XMLDesc() != domain.XMLDesc()):
                            res = {
                                'changed': True,
                                'change_reason': 'config changed',
                            }
                    else:
                        res = {
                            'changed': True,
                            'created': domain.name(),
                        }
                except libvirtError as e:
                    if (e.get_error_code() != 9):
                        module.fail_json(msg=('libvirtError: %s' % e.message))
                if ((autostart is not None) and v.autostart(domain_name, autostart)):
                    res = {
                        'changed': True,
                        'change_reason': 'autostart',
                    }
            elif (not guest):
                module.fail_json(msg=('%s requires 1 argument: guest' % command))
            else:
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
            module.fail_json(msg=('Command %s not recognized' % command))
    module.fail_json(msg='expected state or command parameter to be specified')