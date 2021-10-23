def get_environment_config(self):
    '\n        :rtype: CloudEnvironmentConfig\n        '
    parser = ConfigParser()
    parser.read(self.config_path)
    ansible_vars = dict(resource_prefix=self.resource_prefix)
    ansible_vars.update(dict(parser.items('default')))
    env_vars = {
        'ANSIBLE_DEBUG_BOTOCORE_LOGS': 'True',
    }
    return CloudEnvironmentConfig(env_vars=env_vars, ansible_vars=ansible_vars, callback_plugins=['aws_resource_actions'])