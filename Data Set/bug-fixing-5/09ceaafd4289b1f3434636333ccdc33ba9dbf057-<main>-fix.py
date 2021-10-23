def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='str', aliases=['host']), key=dict(required=False, type='str'), path=dict(default='~/.ssh/known_hosts', type='path'), hash_host=dict(required=False, type='bool', default=False), state=dict(default='present', choices=['absent', 'present'])), supports_check_mode=True)
    results = enforce_state(module, module.params)
    module.exit_json(**results)