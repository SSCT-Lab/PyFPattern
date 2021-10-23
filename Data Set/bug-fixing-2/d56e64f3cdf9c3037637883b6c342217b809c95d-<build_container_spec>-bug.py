

def build_container_spec(self):
    mounts = None
    if (self.mounts is not None):
        mounts = []
        for mount_config in self.mounts:
            mount_options = {
                'target': 'target',
                'source': 'source',
                'type': 'type',
                'readonly': 'read_only',
                'propagation': 'propagation',
                'labels': 'labels',
                'no_copy': 'no_copy',
                'driver_config': 'driver_config',
                'tmpfs_size': 'tmpfs_size',
                'tmpfs_mode': 'tmpfs_mode',
            }
            mount_args = {
                
            }
            for (option, mount_arg) in mount_options.items():
                value = mount_config.get(option)
                if (value is not None):
                    mount_args[mount_arg] = value
            mounts.append(types.Mount(**mount_args))
    configs = None
    if (self.configs is not None):
        configs = []
        for config_config in self.configs:
            configs.append(types.ConfigReference(config_id=config_config['config_id'], config_name=config_config['config_name'], filename=config_config.get('filename'), uid=config_config.get('uid'), gid=config_config.get('gid'), mode=config_config.get('mode')))
    secrets = None
    if (self.secrets is not None):
        secrets = []
        for secret_config in self.secrets:
            secrets.append(types.SecretReference(secret_id=secret_config['secret_id'], secret_name=secret_config['secret_name'], filename=secret_config.get('filename'), uid=secret_config.get('uid'), gid=secret_config.get('gid'), mode=secret_config.get('mode')))
    dns_config_args = {
        
    }
    if (self.dns is not None):
        dns_config_args['nameservers'] = self.dns
    if (self.dns_search is not None):
        dns_config_args['search'] = self.dns_search
    if (self.dns_options is not None):
        dns_config_args['options'] = self.dns_options
    dns_config = (types.DNSConfig(**dns_config_args) if dns_config_args else None)
    container_spec_args = {
        
    }
    if (self.command is not None):
        container_spec_args['command'] = self.command
    if (self.args is not None):
        container_spec_args['args'] = self.args
    if (self.env is not None):
        container_spec_args['env'] = self.env
    if (self.user is not None):
        container_spec_args['user'] = self.user
    if (self.container_labels is not None):
        container_spec_args['labels'] = self.container_labels
    if (self.healthcheck is not None):
        container_spec_args['healthcheck'] = types.Healthcheck(**self.healthcheck)
    if (self.hostname is not None):
        container_spec_args['hostname'] = self.hostname
    if (self.hosts is not None):
        container_spec_args['hosts'] = self.hosts
    if (self.read_only is not None):
        container_spec_args['read_only'] = self.read_only
    if (self.stop_grace_period is not None):
        container_spec_args['stop_grace_period'] = self.stop_grace_period
    if (self.stop_signal is not None):
        container_spec_args['stop_signal'] = self.stop_signal
    if (self.tty is not None):
        container_spec_args['tty'] = self.tty
    if (self.groups is not None):
        container_spec_args['groups'] = self.groups
    if (self.working_dir is not None):
        container_spec_args['workdir'] = self.working_dir
    if (secrets is not None):
        container_spec_args['secrets'] = secrets
    if (mounts is not None):
        container_spec_args['mounts'] = mounts
    if (dns_config is not None):
        container_spec_args['dns_config'] = dns_config
    if (configs is not None):
        container_spec_args['configs'] = configs
    return types.ContainerSpec(self.image, **container_spec_args)
