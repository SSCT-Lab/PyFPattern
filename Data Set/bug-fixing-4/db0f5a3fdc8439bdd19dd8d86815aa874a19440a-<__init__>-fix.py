def __init__(self):
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), element_username=dict(required=True, aliases=['account_id'], type='str'), from_name=dict(required=False, default=None), initiator_secret=dict(required=False, type='str'), target_secret=dict(required=False, type='str'), attributes=dict(required=False, type='dict'), status=dict(required=False, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    params = self.module.params
    self.state = params.get('state')
    self.element_username = params.get('element_username')
    self.from_name = params.get('from_name')
    self.initiator_secret = params.get('initiator_secret')
    self.target_secret = params.get('target_secret')
    self.attributes = params.get('attributes')
    self.status = params.get('status')
    if (HAS_SF_SDK is False):
        self.module.fail_json(msg='Unable to import the Element SW Python SDK')
    else:
        self.sfe = netapp_utils.create_sf_connection(module=self.module)
    self.elementsw_helper = NaElementSWModule(self.sfe)
    if (self.attributes is not None):
        self.attributes.update(self.elementsw_helper.set_element_attributes(source='na_elementsw_account'))
    else:
        self.attributes = self.elementsw_helper.set_element_attributes(source='na_elementsw_account')