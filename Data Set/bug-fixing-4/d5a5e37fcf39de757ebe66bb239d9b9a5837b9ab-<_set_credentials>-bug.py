def _set_credentials(self):
    '\n            :param config_data: contents of the inventory config file\n        '
    self.boto_profile = self._options.get('boto_profile')
    self.aws_access_key_id = self._options.get('aws_access_key_id')
    self.aws_secret_access_key = self._options.get('aws_secret_access_key')
    self.aws_security_token = self._options.get('aws_security_token')
    if ((not self.boto_profile) and (not (self.aws_access_key_id and self.aws_secret_access_key))):
        raise AnsibleError('Insufficient boto credentials found. Please provide them in your inventory configuration file or set them as environment variables.')