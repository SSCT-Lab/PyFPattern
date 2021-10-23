def __init__(self, **kwargs):
    local_settings = {
        
    }
    for key in AnsibleAWSModule.default_settings:
        try:
            local_settings[key] = kwargs.pop(key)
        except KeyError:
            local_settings[key] = AnsibleAWSModule.default_settings[key]
    self.settings = local_settings
    if local_settings['default_args']:
        argument_spec_full = ec2_argument_spec()
        try:
            argument_spec_full.update(kwargs['argument_spec'])
        except (TypeError, NameError):
            pass
        kwargs['argument_spec'] = argument_spec_full
    self._module = AnsibleAWSModule.default_settings['module_class'](**kwargs)
    if (local_settings['check_boto3'] and (not HAS_BOTO3)):
        self._module.fail_json(msg='Python modules "botocore" or "boto3" are missing, please install both')
    self.check_mode = self._module.check_mode