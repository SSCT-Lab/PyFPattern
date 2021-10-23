def main():
    argument_spec = dict(registry_url=dict(type='str', required=False, default=DEFAULT_DOCKER_REGISTRY, aliases=['registry', 'url']), username=dict(type='str', required=False), password=dict(type='str', required=False, no_log=True), email=dict(type='str'), reauthorize=dict(type='bool', default=False, aliases=['reauth']), state=dict(type='str', default='present', choices=['present', 'absent']), config_path=dict(type='path', default='~/.docker/config.json', aliases=['self.config_path', 'dockercfg_path']))
    required_if = [('state', 'present', ['username', 'password'])]
    client = AnsibleDockerClient(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)
    results = dict(changed=False, actions=[], login_result={
        
    })
    if ((client.module.params['state'] == 'present') and (client.module.params['registry_url'] == DEFAULT_DOCKER_REGISTRY) and (not client.module.params['email'])):
        client.module.fail_json(msg="'email' is required when logging into DockerHub")
    LoginManager(client, results)
    if ('actions' in results):
        del results['actions']
    client.module.exit_json(**results)