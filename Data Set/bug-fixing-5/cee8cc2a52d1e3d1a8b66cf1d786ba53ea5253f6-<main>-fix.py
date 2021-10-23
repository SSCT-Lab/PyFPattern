def main():
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), key=dict(required=True, type='str'), validate_certs=dict(default='yes', type='bool')), supports_check_mode=True)
    RpmKey(module)