

def main():
    argument_spec = dict(source=dict(type='str', choices=['build', 'load', 'pull', 'local']), build=dict(type='dict', suboptions=dict(cache_from=dict(type='list', elements='str'), container_limits=dict(type='dict', options=dict(memory=dict(type='int'), memswap=dict(type='int'), cpushares=dict(type='int'), cpusetcpus=dict(type='str'))), dockerfile=dict(type='str'), http_timeout=dict(type='int'), network=dict(type='str'), nocache=dict(type='bool', default=False), path=dict(type='path', required=True), pull=dict(type='bool'), rm=dict(type='bool', default=True), args=dict(type='dict'), use_config_proxy=dict(type='bool'))), archive_path=dict(type='path'), container_limits=dict(type='dict', options=dict(memory=dict(type='int'), memswap=dict(type='int'), cpushares=dict(type='int'), cpusetcpus=dict(type='str')), removedin_version='2.12'), dockerfile=dict(type='str', removedin_version='2.12'), force=dict(type='bool', removed_in_version='2.12'), force_source=dict(type='bool', default=False), force_absent=dict(type='bool', default=False), force_tag=dict(type='bool', default=False), http_timeout=dict(type='int', removedin_version='2.12'), load_path=dict(type='path'), name=dict(type='str', required=True), nocache=dict(type='bool', default=False, removedin_version='2.12'), path=dict(type='path', aliases=['build_path'], removedin_version='2.12'), pull=dict(type='bool', removedin_version='2.12'), push=dict(type='bool', default=False), repository=dict(type='str'), rm=dict(type='bool', default=True, removedin_version='2.12'), state=dict(type='str', default='present', choices=['absent', 'present', 'build']), tag=dict(type='str', default='latest'), use_tls=dict(type='str', choices=['no', 'encrypt', 'verify'], removed_in_version='2.11'), buildargs=dict(type='dict', removedin_version='2.12'))
    required_if = [('source', 'load', ['load_path'])]

    def detect_build_cache_from(client):
        return (client.params['build'] and (client.params['build']['cache_from'] is not None))

    def detect_build_network(client):
        return (client.params['build'] and (client.params['build']['network'] is not None))

    def detect_use_config_proxy(client):
        return (client.params['build'] and (client.params['build']['use_config_proxy'] is not None))
    option_minimal_versions = dict()
    option_minimal_versions['build.cache_from'] = dict(docker_py_version='2.1.0', docker_api_version='1.25', detect_usage=detect_build_cache_from)
    option_minimal_versions['build.network'] = dict(docker_py_version='2.4.0', docker_api_version='1.25', detect_usage=detect_build_network)
    option_minimal_versions['build.use_config_proxy'] = dict(docker_py_version='3.7.0', detect_usage=detect_use_config_proxy)
    client = AnsibleDockerClient(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True, min_docker_version='1.8.0', min_docker_api_version='1.20', option_minimal_versions=option_minimal_versions)
    if (client.module.params['state'] == 'build'):
        client.module.warn('The "build" state has been deprecated for a long time and will be removed in Ansible 2.11. Please use "present", which has the same meaning as "build".')
        client.module.params['state'] = 'present'
    if client.module.params['use_tls']:
        client.module.warn('The "use_tls" option has been deprecated for a long time and will be removed in Ansible 2.11. Please use the"tls" and "tls_verify" options instead.')
    build_options = dict(container_limits='container_limits', dockerfile='dockerfile', http_timeout='http_timeout', nocache='nocache', path='path', pull='pull', rm='rm', buildargs='args')
    for (option, build_option) in build_options.items():
        default_value = None
        if (option in ('rm',)):
            default_value = True
        elif (option in ('nocache',)):
            default_value = False
        if (client.module.params[option] != default_value):
            if (client.module.params['build'] is None):
                client.module.params['build'] = dict()
            if (client.module.params['build'].get(build_option) != default_value):
                client.fail(('Cannot specify both %s and build.%s!' % (option, build_option)))
            client.module.params['build'][build_option] = client.module.params[option]
            client.module.warn(('Please specify build.%s instead of %s. The %s option has been renamed and will be removed in Ansible 2.12.' % (build_option, option, option)))
    if (client.module.params['source'] == 'build'):
        if ((not client.module.params['build']) or (not client.module.params['build'].get('path'))):
            client.module.fail('If "source" is set to "build", the "build.path" option must be specified.')
        if (client.module.params['build']['pull'] is None):
            client.module.warn("The default for build.pull is currently 'yes', but will be changed to 'no' in Ansible 2.12. Please set build.pull explicitly to the value you need.")
            client.module.params['build']['pull'] = True
    if ((client.module.params['state'] == 'present') and (client.module.params['source'] is None)):
        if (client.module.params['build'] or dict()).get('path'):
            client.module.params['source'] = 'build'
        elif client.module.params['load_path']:
            client.module.params['source'] = 'load'
        else:
            client.module.params['source'] = 'pull'
        client.module.warn(('The value of the "source" option was determined to be "%s". Please set the "source" option explicitly. Autodetection will be removed in Ansible 2.12.' % client.module.params['source']))
    if client.module.params['force']:
        client.module.params['force_source'] = True
        client.module.params['force_absent'] = True
        client.module.params['force_tag'] = True
        client.module.warn('The "force" option will be removed in Ansible 2.12. Please use the "force_source", "force_absent" or "force_tag" option instead, depending on what you want to force.')
    results = dict(changed=False, actions=[], image={
        
    })
    ImageManager(client, results)
    client.module.exit_json(**results)
