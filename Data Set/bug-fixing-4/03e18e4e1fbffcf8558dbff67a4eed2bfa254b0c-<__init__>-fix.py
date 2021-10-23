def __init__(self):
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(management_virtual_ip=dict(required=True, type='str'), storage_virtual_ip=dict(required=True, type='str'), replica_count=dict(required=False, type='str', default='2'), cluster_admin_username=dict(required=False, type='str'), cluster_admin_password=dict(required=False, type='str', no_log=True), accept_eula=dict(required=False, type='bool'), nodes=dict(required=True, type=list), attributes=dict(required=False, type='dict', default=None)))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    input_params = self.module.params
    self.management_virtual_ip = input_params['management_virtual_ip']
    self.storage_virtual_ip = input_params['storage_virtual_ip']
    self.replica_count = input_params['replica_count']
    self.accept_eula = input_params.get('accept_eula')
    self.attributes = input_params.get('attributes')
    self.nodes = input_params['nodes']
    self.cluster_admin_username = input_params.get('cluster_admin_username')
    self.cluster_admin_password = input_params.get('cluster_admin_password')
    if (HAS_SF_SDK is False):
        self.module.fail_json(msg='Unable to import the SolidFire Python SDK')
    else:
        self.sfe = netapp_utils.create_sf_connection(module=self.module)
    self.elementsw_helper = NaElementSWModule(self.sfe)
    if (self.attributes is not None):
        self.attributes.update(self.elementsw_helper.set_element_attributes(source='na_elementsw_cluster'))
    else:
        self.attributes = self.elementsw_helper.set_element_attributes(source='na_elementsw_cluster')