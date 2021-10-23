

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='str'), state=dict(required=False, type='str', choices=['present', 'absent'], default='present')), supports_check_mode=True)
    Icinga2FeatureHelper(module).manage()
