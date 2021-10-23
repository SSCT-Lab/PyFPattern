

def main():
    argument_spec = dict(name=dict(type='str', required=True), image=dict(type='str'), state=dict(type='str', default='present', choices=['present', 'absent']), mounts=dict(type='list', elements='dict', options=dict(source=dict(type='str', required=True), target=dict(type='str', required=True), type=dict(type='str', default='bind', choices=['bind', 'volume', 'tmpfs']), readonly=dict(type='bool', default=False))), configs=dict(type='list', elements='dict', options=dict(config_id=dict(type='str', required=True), config_name=dict(type='str', required=True), filename=dict(type='str'), uid=dict(type='int', default=0), gid=dict(type='int', default=0), mode=dict(type='int', default=292))), secrets=dict(type='list', elements='dict', options=dict(secret_id=dict(type='str', required=True), secret_name=dict(type='str', required=True), filename=dict(type='str'), uid=dict(type='int', default=0), gid=dict(type='int', default=0), mode=dict(type='int', default=292))), networks=dict(type='list', elements='str'), command=dict(type='raw'), args=dict(type='list', elements='str'), env=dict(type='raw'), env_files=dict(type='list', elements='path'), force_update=dict(type='bool', default=False), groups=dict(type='list', elements='str'), log_driver=dict(type='str'), log_driver_options=dict(type='dict'), publish=dict(type='list', elements='dict', options=dict(published_port=dict(type='int', required=True), target_port=dict(type='int', required=True), protocol=dict(type='str', default='tcp', choices=('tcp', 'udp')), mode=dict(type='str', choices=('ingress', 'host')))), constraints=dict(type='list'), placement_preferences=dict(type='list'), tty=dict(type='bool'), dns=dict(type='list'), dns_search=dict(type='list'), dns_options=dict(type='list'), healthcheck=dict(type='dict', options=dict(test=dict(type='raw'), interval=dict(type='str'), timeout=dict(type='str'), start_period=dict(type='str'), retries=dict(type='int'))), hostname=dict(type='str'), labels=dict(type='dict'), container_labels=dict(type='dict'), mode=dict(type='str', default='replicated'), replicas=dict(type='int', default=(- 1)), endpoint_mode=dict(type='str', choices=['vip', 'dnsrr']), stop_grace_period=dict(type='str'), stop_signal=dict(type='str'), limit_cpu=dict(type='float'), limit_memory=dict(type='str'), reserve_cpu=dict(type='float'), reserve_memory=dict(type='str'), resolve_image=dict(type='bool', default=True), restart_policy=dict(type='str', choices=['none', 'on-failure', 'any']), restart_policy_delay=dict(type='raw'), restart_policy_attempts=dict(type='int'), restart_policy_window=dict(type='raw'), update_delay=dict(type='raw'), update_parallelism=dict(type='int'), update_failure_action=dict(type='str', choices=['continue', 'pause']), update_monitor=dict(type='raw'), update_max_failure_ratio=dict(type='float'), update_order=dict(type='str', choices=['stop-first', 'start-first']), user=dict(type='str'), working_dir=dict(type='str'))
    option_minimal_versions = dict(dns=dict(docker_py_version='2.6.0', docker_api_version='1.25'), dns_options=dict(docker_py_version='2.6.0', docker_api_version='1.25'), dns_search=dict(docker_py_version='2.6.0', docker_api_version='1.25'), endpoint_mode=dict(docker_py_version='3.0.0', docker_api_version='1.25'), force_update=dict(docker_py_version='2.1.0', docker_api_version='1.25'), healthcheck=dict(docker_py_version='2.0.0', docker_api_version='1.25'), hostname=dict(docker_py_version='2.2.0', docker_api_version='1.25'), groups=dict(docker_py_version='2.6.0', docker_api_version='1.25'), tty=dict(docker_py_version='2.4.0', docker_api_version='1.25'), secrets=dict(docker_py_version='2.1.0', docker_api_version='1.25'), configs=dict(docker_py_version='2.6.0', docker_api_version='1.30'), update_max_failure_ratio=dict(docker_py_version='2.1.0', docker_api_version='1.25'), update_monitor=dict(docker_py_version='2.1.0', docker_api_version='1.25'), update_order=dict(docker_py_version='2.7.0', docker_api_version='1.29'), stop_signal=dict(docker_py_version='2.6.0', docker_api_version='1.28'), placement_preferences=dict(docker_py_version='2.4.0', docker_api_version='1.27'), publish=dict(docker_py_version='3.0.0', docker_api_version='1.25'), publish_mode=dict(docker_py_version='3.0.0', docker_api_version='1.25', detect_usage=_detect_publish_mode_usage, usage_msg='set publish.mode'), healthcheck_start_period=dict(docker_py_version='2.4.0', docker_api_version='1.25', detect_usage=_detect_healthcheck_start_period, usage_msg='set healthcheck.start_period'))
    required_if = [('state', 'present', ['image'])]
    client = AnsibleDockerClient(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True, min_docker_version='2.0.0', min_docker_api_version='1.24', option_minimal_versions=option_minimal_versions)
    dsm = DockerServiceManager(client)
    (msg, changed, rebuilt, changes, facts) = dsm.run_safe()
    results = dict(msg=msg, changed=changed, rebuilt=rebuilt, changes=changes, ansible_docker_service=facts)
    if client.module._diff:
        (before, after) = dsm.diff_tracker.get_before_after()
        results['diff'] = dict(before=before, after=after)
    client.module.exit_json(**results)
