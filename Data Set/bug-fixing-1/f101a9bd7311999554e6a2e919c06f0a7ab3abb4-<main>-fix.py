

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='str'), state=dict(required=False, type='str', choices=['present', 'absent'], default='present')), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    Icinga2FeatureHelper(module).manage()
