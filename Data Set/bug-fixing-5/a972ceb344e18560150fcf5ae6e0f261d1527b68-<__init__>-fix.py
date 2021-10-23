def __init__(self):
    '\n            Setup Ansible parameters and SolidFire connection\n        '
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(src_volume_id=dict(aliases=['volume_id'], required=True, type='str'), dest_hostname=dict(required=False, type='str'), dest_username=dict(required=False, type='str'), dest_password=dict(required=False, type='str', no_log=True), dest_volume_id=dict(required=True, type='str'), format=dict(required=False, choices=['native', 'uncompressed'], default='native'), script=dict(required=False, type='str'), script_parameters=dict(required=False, type='dict')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_together=[['script', 'script_parameters']], supports_check_mode=True)
    if (HAS_SF_SDK is False):
        self.module.fail_json(msg='Unable to import the SolidFire Python SDK')
    if (self.module.params['dest_hostname'] is None):
        self.module.params['dest_hostname'] = self.module.params['hostname']
    if (self.module.params['dest_username'] is None):
        self.module.params['dest_username'] = self.module.params['username']
    if (self.module.params['dest_password'] is None):
        self.module.params['dest_password'] = self.module.params['password']
    params = self.module.params
    self.src_connection = netapp_utils.create_sf_connection(self.module)
    self.module.params['username'] = params['dest_username']
    self.module.params['password'] = params['dest_password']
    self.module.params['hostname'] = params['dest_hostname']
    self.dest_connection = netapp_utils.create_sf_connection(self.module)
    self.elementsw_helper = NaElementSWModule(self.src_connection)
    self.attributes = self.elementsw_helper.set_element_attributes(source='na_elementsw_backup')