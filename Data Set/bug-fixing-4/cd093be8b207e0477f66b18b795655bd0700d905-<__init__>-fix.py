def __init__(self):
    '\n            Setup Ansible parameters and ElementSW connection\n        '
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=False, type='str'), vlan_tag=dict(required=True, type='str'), svip=dict(required=False, type='str'), netmask=dict(required=False, type='str'), gateway=dict(required=False, type='str'), namespace=dict(required=False, type='bool'), attributes=dict(required=False, type='dict'), address_blocks=dict(required=False, type='list')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    if (HAS_SF_SDK is False):
        self.module.fail_json(msg='Unable to import the SolidFire Python SDK')
    else:
        self.elem = netapp_utils.create_sf_connection(module=self.module)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    self.elementsw_helper = NaElementSWModule(self.elem)
    if (self.parameters.get('attributes') is not None):
        self.parameters['attributes'].update(self.elementsw_helper.set_element_attributes(source='na_elementsw_vlan'))
    else:
        self.parameters['attributes'] = self.elementsw_helper.set_element_attributes(source='na_elementsw_vlan')