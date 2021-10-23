

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(aliases=['key'], required=True), value=dict(aliases=['val'], required=False, type='str'), state=dict(default='present', choices=['present', 'absent']), reload=dict(default=True, type='bool'), sysctl_set=dict(default=False, type='bool'), ignoreerrors=dict(default=False, type='bool'), sysctl_file=dict(default='/etc/sysctl.conf', type='path')), supports_check_mode=True, required_if=[('state', 'present', ['value'])])
    if (module.params['name'] is None):
        module.fail_json(msg='name can not be None')
    if ((module.params['state'] == 'present') and (module.params['value'] is None)):
        module.fail_json(msg='value can not be None')
    if (module.params['name'] == ''):
        module.fail_json(msg='name can not be blank')
    if ((module.params['state'] == 'present') and (module.params['value'] == '')):
        module.fail_json(msg='value can not be blank')
    result = SysctlModule(module)
    module.exit_json(changed=result.changed)
