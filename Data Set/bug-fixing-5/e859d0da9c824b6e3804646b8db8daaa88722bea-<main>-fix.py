def main():
    argument_spec = dict(name=dict(type='str', required=True), state=dict(type='str', choices=['absent', 'present'], default='present'), data=dict(type='str', no_log=True), labels=dict(type='dict'), force=dict(type='bool', default=False))
    required_if = [('state', 'present', ['data'])]
    client = AnsibleDockerClient(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)
    results = dict(changed=False, secret_id='')
    SecretManager(client, results)()
    client.module.exit_json(**results)