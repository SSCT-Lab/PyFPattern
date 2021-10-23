def main():
    argument_spec = dict(auto_remove=dict(type='bool', default=False), blkio_weight=dict(type='int'), capabilities=dict(type='list'), cleanup=dict(type='bool', default=False), command=dict(type='raw'), cpu_period=dict(type='int'), cpu_quota=dict(type='int'), cpuset_cpus=dict(type='str'), cpuset_mems=dict(type='str'), cpu_shares=dict(type='int'), detach=dict(type='bool', default=True), devices=dict(type='list'), dns_servers=dict(type='list'), dns_opts=dict(type='list'), dns_search_domains=dict(type='list'), env=dict(type='dict'), env_file=dict(type='path'), entrypoint=dict(type='list'), etc_hosts=dict(type='dict'), exposed_ports=dict(type='list', aliases=['exposed', 'expose']), force_kill=dict(type='bool', default=False, aliases=['forcekill']), groups=dict(type='list'), hostname=dict(type='str'), ignore_image=dict(type='bool', default=False), image=dict(type='str'), interactive=dict(type='bool', default=False), ipc_mode=dict(type='str'), keep_volumes=dict(type='bool', default=True), kernel_memory=dict(type='str'), kill_signal=dict(type='str'), labels=dict(type='dict'), links=dict(type='list'), log_driver=dict(type='str', choices=['none', 'json-file', 'syslog', 'journald', 'gelf', 'fluentd', 'awslogs', 'splunk'], default=None), log_options=dict(type='dict', aliases=['log_opt']), mac_address=dict(type='str'), memory=dict(type='str', default='0'), memory_reservation=dict(type='str'), memory_swap=dict(type='str'), memory_swappiness=dict(type='int'), name=dict(type='str', required=True), network_mode=dict(type='str'), networks=dict(type='list'), oom_killer=dict(type='bool'), oom_score_adj=dict(type='int'), paused=dict(type='bool', default=False), pid_mode=dict(type='str'), privileged=dict(type='bool', default=False), published_ports=dict(type='list', aliases=['ports']), pull=dict(type='bool', default=False), purge_networks=dict(type='bool', default=False), read_only=dict(type='bool', default=False), recreate=dict(type='bool', default=False), restart=dict(type='bool', default=False), restart_policy=dict(type='str', choices=['no', 'on-failure', 'always', 'unless-stopped']), restart_retries=dict(type='int', default=None), shm_size=dict(type='str'), security_opts=dict(type='list'), state=dict(type='str', choices=['absent', 'present', 'started', 'stopped'], default='started'), stop_signal=dict(type='str'), stop_timeout=dict(type='int'), trust_image_content=dict(type='bool', default=False), tty=dict(type='bool', default=False), ulimits=dict(type='list'), user=dict(type='str'), uts=dict(type='str'), volumes=dict(type='list'), volumes_from=dict(type='list'), volume_driver=dict(type='str'))
    required_if = [('state', 'present', ['image'])]
    client = AnsibleDockerClient(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True)
    if ((not HAS_DOCKER_PY_2) and client.module.params.get('auto_remove')):
        client.module.fail_json(msg="'auto_remove' is not compatible with docker-py, and requires the docker python module")
    cm = ContainerManager(client)
    client.module.exit_json(**cm.results)