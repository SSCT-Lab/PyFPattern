def has_different_configuration(self, image):
    '\n        Diff parameters vs existing container config. Returns tuple: (True | False, List of differences)\n        '
    self.log('Starting has_different_configuration')
    self.parameters.expected_entrypoint = self._get_expected_entrypoint()
    self.parameters.expected_links = self._get_expected_links()
    self.parameters.expected_ports = self._get_expected_ports()
    self.parameters.expected_exposed = self._get_expected_exposed(image)
    self.parameters.expected_volumes = self._get_expected_volumes(image)
    self.parameters.expected_binds = self._get_expected_binds(image)
    self.parameters.expected_ulimits = self._get_expected_ulimits(self.parameters.ulimits)
    self.parameters.expected_etc_hosts = self._convert_simple_dict_to_list('etc_hosts')
    self.parameters.expected_env = self._get_expected_env(image)
    self.parameters.expected_cmd = self._get_expected_cmd()
    self.parameters.expected_devices = self._get_expected_devices()
    if (not self.container.get('HostConfig')):
        self.fail('has_config_diff: Error parsing container properties. HostConfig missing.')
    if (not self.container.get('Config')):
        self.fail('has_config_diff: Error parsing container properties. Config missing.')
    if (not self.container.get('NetworkSettings')):
        self.fail('has_config_diff: Error parsing container properties. NetworkSettings missing.')
    host_config = self.container['HostConfig']
    log_config = host_config.get('LogConfig', dict())
    restart_policy = host_config.get('RestartPolicy', dict())
    config = self.container['Config']
    network = self.container['NetworkSettings']
    detach = (not (config.get('AttachStderr') and config.get('AttachStdout')))
    if (config.get('ExposedPorts') is not None):
        expected_exposed = [re.sub('/.+$', '', p) for p in config.get('ExposedPorts', dict()).keys()]
    else:
        expected_exposed = []
    config_mapping = dict(image=config.get('Image'), expected_cmd=config.get('Cmd'), hostname=config.get('Hostname'), user=config.get('User'), detach=detach, interactive=config.get('OpenStdin'), capabilities=host_config.get('CapAdd'), expected_devices=host_config.get('Devices'), dns_servers=host_config.get('Dns'), dns_opts=host_config.get('DnsOptions'), dns_search_domains=host_config.get('DnsSearch'), expected_env=(config.get('Env') or []), expected_entrypoint=config.get('Entrypoint'), expected_etc_hosts=host_config['ExtraHosts'], expected_exposed=expected_exposed, groups=host_config.get('GroupAdd'), ipc_mode=host_config.get('IpcMode'), labels=config.get('Labels'), expected_links=host_config.get('Links'), log_driver=log_config.get('Type'), log_options=log_config.get('Config'), mac_address=network.get('MacAddress'), memory_swappiness=host_config.get('MemorySwappiness'), network_mode=host_config.get('NetworkMode'), oom_killer=host_config.get('OomKillDisable'), oom_score_adj=host_config.get('OomScoreAdj'), pid_mode=host_config.get('PidMode'), privileged=host_config.get('Privileged'), expected_ports=host_config.get('PortBindings'), read_only=host_config.get('ReadonlyRootfs'), restart_policy=restart_policy.get('Name'), restart_retries=restart_policy.get('MaximumRetryCount'), security_opts=host_config.get('SecuriytOpt'), stop_signal=config.get('StopSignal'), tty=config.get('Tty'), expected_ulimits=host_config.get('Ulimits'), uts=host_config.get('UTSMode'), expected_volumes=config.get('Volumes'), expected_binds=host_config.get('Binds'), volumes_from=host_config.get('VolumesFrom'), volume_driver=host_config.get('VolumeDriver'))
    differences = []
    for (key, value) in config_mapping.items():
        self.log(('check differences %s %s vs %s' % (key, getattr(self.parameters, key), str(value))))
        if (getattr(self.parameters, key, None) is not None):
            if (isinstance(getattr(self.parameters, key), list) and isinstance(value, list)):
                if ((len(getattr(self.parameters, key)) > 0) and isinstance(getattr(self.parameters, key)[0], dict)):
                    self.log(('comparing list of dict: %s' % key))
                    match = self._compare_dictionary_lists(getattr(self.parameters, key), value)
                else:
                    self.log(('comparing lists: %s' % key))
                    set_a = set(getattr(self.parameters, key))
                    set_b = set(value)
                    match = (set_a <= set_b)
            elif (isinstance(getattr(self.parameters, key), list) and (not len(getattr(self.parameters, key))) and (value is None)):
                continue
            elif (isinstance(getattr(self.parameters, key), dict) and isinstance(value, dict)):
                self.log(('comparing two dicts: %s' % key))
                match = self._compare_dicts(getattr(self.parameters, key), value)
            elif (isinstance(getattr(self.parameters, key), dict) and (not len(list(getattr(self.parameters, key).keys()))) and (value is None)):
                continue
            else:
                self.log(('primitive compare: %s' % key))
                match = (getattr(self.parameters, key) == value)
            if (not match):
                item = dict()
                item[key] = dict(parameter=getattr(self.parameters, key), container=value)
                differences.append(item)
    has_differences = (True if (len(differences) > 0) else False)
    return (has_differences, differences)