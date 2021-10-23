def __init__(self):
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), element_username=dict(required=True, type='str'), account_id=dict(required=False, type='int', default=None), new_element_username=dict(required=False, type='str', default=None), initiator_secret=dict(required=False, type='str'), target_secret=dict(required=False, type='str'), attributes=dict(required=False, type='dict'), status=dict(required=False, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    params = self.module.params
    self.state = params['state']
    self.element_username = params['element_username']
    self.account_id = params['account_id']
    self.new_element_username = params['new_element_username']
    self.initiator_secret = params['initiator_secret']
    self.target_secret = params['target_secret']
    self.attributes = params['attributes']
    self.status = params['status']
    if (HAS_SF_SDK is False):
        self.module.fail_json(msg='Unable to import the Element SW Python SDK')
    else:
        self.sfe = netapp_utils.create_sf_connection(module=self.module)
    self.elementsw_helper = NaElementSWModule(self.sfe)
    if (self.attributes is not None):
        self.attributes.update(self.elementsw_helper.set_element_attributes(source='na_elementsw_account'))
    else:
        self.attributes = self.elementsw_helper.set_element_attributes(source='na_elementsw_account')