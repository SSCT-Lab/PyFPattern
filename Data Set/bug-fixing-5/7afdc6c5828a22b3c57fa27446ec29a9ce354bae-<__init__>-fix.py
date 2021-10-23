def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, type='str', choices=['present', 'absent'], default='present'), vserver=dict(required=True, type='str'), peer_vserver=dict(required=True, type='str'), peer_cluster=dict(required=False, type='str'), applications=dict(required=False, type='list', choices=['snapmirror', 'file_copy', 'lun_copy', 'flexcache']), dest_hostname=dict(required=False, type='str'), dest_username=dict(required=False, type='str'), dest_password=dict(required=False, type='str', no_log=True)))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)
        if self.parameters.get('dest_hostname'):
            self.module.params['hostname'] = self.parameters['dest_hostname']
            if self.parameters.get('dest_username'):
                self.module.params['username'] = self.parameters['dest_username']
            if self.parameters.get('dest_password'):
                self.module.params['password'] = self.parameters['dest_password']
            self.dest_server = netapp_utils.setup_na_ontap_zapi(module=self.module)
            self.module.params['hostname'] = self.parameters['hostname']