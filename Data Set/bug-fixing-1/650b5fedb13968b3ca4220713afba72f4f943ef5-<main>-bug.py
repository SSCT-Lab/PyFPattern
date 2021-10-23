

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(aliases=['key'], required=True), value=dict(aliases=['val'], required=False, type='str'), state=dict(default='present', choices=['present', 'absent']), reload=dict(default=True, type='bool'), sysctl_set=dict(default=False, type='bool'), ignoreerrors=dict(default=False, type='bool'), sysctl_file=dict(default='/etc/sysctl.conf', type='path')), supports_check_mode=True)
    result = SysctlModule(module)
    module.exit_json(changed=result.changed)
