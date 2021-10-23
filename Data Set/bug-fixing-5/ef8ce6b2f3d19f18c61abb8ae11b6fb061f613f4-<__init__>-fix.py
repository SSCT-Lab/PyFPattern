def __init__(self):
    self.module_arg_spec = dict(secret_name=dict(type='str', required=True), secret_value=dict(type='str', no_log=True), keyvault_uri=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']))
    required_if = [('state', 'present', ['secret_value'])]
    self.results = dict(changed=False, state=dict())
    self.secret_name = None
    self.secret_value = None
    self.keyvault_uri = None
    self.state = None
    self.data_creds = None
    self.client = None
    self.tags = None
    super(AzureRMKeyVaultSecret, self).__init__(self.module_arg_spec, supports_check_mode=True, required_if=required_if, supports_tags=True)