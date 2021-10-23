def main():
    argument_spec = dict(network_name=dict(type='str', required=True, aliases=['name']), connected=dict(type='list', default=[], elements='str', aliases=['containers']), state=dict(type='str', default='present', choices=['present', 'absent']), driver=dict(type='str', default='bridge'), driver_options=dict(type='dict', default={
        
    }), force=dict(type='bool', default=False), appends=dict(type='bool', default=False, aliases=['incremental']), ipam_driver=dict(type='str'), ipam_driver_options=dict(type='dict'), ipam_options=dict(type='dict', default={
        
    }, options=dict(subnet=dict(type='str'), iprange=dict(type='str'), gateway=dict(type='str'), aux_addresses=dict(type='dict')), removed_in_version='2.12'), ipam_config=dict(type='list', elements='dict', options=dict(subnet=dict(type='str'), iprange=dict(type='str'), gateway=dict(type='str'), aux_addresses=dict(type='dict'))), enable_ipv6=dict(type='bool'), internal=dict(type='bool'), labels=dict(type='dict', default={
        
    }), debug=dict(type='bool', default=False), scope=dict(type='str', choices=['local', 'global', 'swarm']), attachable=dict(type='bool'))
    mutually_exclusive = [('ipam_config', 'ipam_options')]
    option_minimal_versions = dict(scope=dict(docker_py_version='2.6.0', docker_api_version='1.30'), attachable=dict(docker_py_version='2.0.0', docker_api_version='1.26'), labels=dict(docker_api_version='1.23'), ipam_driver_options=dict(docker_py_version='2.0.0'))
    client = AnsibleDockerClient(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True, min_docker_version='1.10.0', min_docker_api_version='1.22', option_minimal_versions=option_minimal_versions)
    try:
        cm = DockerNetworkManager(client)
        client.module.exit_json(**cm.results)
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(e), exception=traceback.format_exc())