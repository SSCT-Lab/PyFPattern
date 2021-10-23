

def main():
    argument_spec = url_argument_spec()
    del argument_spec['force']
    argument_spec.update(state=dict(default='present', choices=['absent', 'present']), name=dict(required=True, aliases=['host']), zone=dict(), template=dict(default=None), check_command=dict(default='hostalive'), display_name=dict(default=None), ip=dict(required=True), variables=dict(type='dict', default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    state = module.params['state']
    name = module.params['name']
    zone = module.params['zone']
    template = []
    template.append(name)
    if module.params['template']:
        template.append(module.params['template'])
    check_command = module.params['check_command']
    ip = module.params['ip']
    display_name = module.params['display_name']
    if (not display_name):
        display_name = name
    variables = module.params['variables']
    try:
        icinga = icinga2_api()
        icinga.module = module
        icinga.check_connection()
    except Exception as e:
        module.fail_json(msg=('unable to connect to Icinga. Exception message: %s' % e))
    data = {
        'attrs': {
            'address': ip,
            'display_name': display_name,
            'check_command': check_command,
            'zone': zone,
            'vars': {
                'made_by': 'ansible',
            },
            'templates': template,
        },
    }
    if variables:
        data['attrs']['vars'].update(variables)
    changed = False
    if icinga.exists(name):
        if (state == 'absent'):
            if module.check_mode:
                module.exit_json(changed=True, name=name, data=data)
            else:
                try:
                    ret = icinga.delete(name)
                    if (ret['code'] == 200):
                        changed = True
                    else:
                        module.fail_json(msg=('bad return code deleting host: %s' % ret['data']))
                except Exception as e:
                    module.fail_json(msg=('exception deleting host: ' + str(e)))
        elif icinga.diff(name, data):
            if module.check_mode:
                module.exit_json(changed=False, name=name, data=data)
            del data['attrs']['templates']
            ret = icinga.modify(name, data)
            if (ret['code'] == 200):
                changed = True
            else:
                module.fail_json(msg=('bad return code modifying host: %s' % ret['data']))
    elif (state == 'present'):
        if module.check_mode:
            changed = True
        else:
            try:
                ret = icinga.create(name, data)
                if (ret['code'] == 200):
                    changed = True
                else:
                    module.fail_json(msg=('bad return code creating host: %s' % ret['data']))
            except Exception as e:
                module.fail_json(msg=('exception creating host: ' + str(e)))
    module.exit_json(changed=changed, name=name, data=data)
