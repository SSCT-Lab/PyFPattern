def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, type='str', choices=['present', 'absent'], default='present'), service_state=dict(required=False, choices=['started', 'stopped']), vserver=dict(required=True, type='str'), nfsv3=dict(required=False, default=None, choices=['enabled', 'disabled']), nfsv4=dict(required=False, default=None, choices=['enabled', 'disabled']), nfsv41=dict(required=False, default=None, choices=['enabled', 'disabled'], aliases=['nfsv4.1']), vstorage_state=dict(required=False, default=None, choices=['enabled', 'disabled']), tcp=dict(required=False, default=None, choices=['enabled', 'disabled']), udp=dict(required=False, default=None, choices=['enabled', 'disabled']), nfsv4_id_domain=dict(required=False, type='str', default=None)))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.service_state = parameters['service_state']
    self.vserver = parameters['vserver']
    self.nfsv3 = parameters['nfsv3']
    self.nfsv4 = parameters['nfsv4']
    self.nfsv41 = parameters['nfsv41']
    self.vstorage_state = parameters['vstorage_state']
    self.nfsv4_id_domain = parameters['nfsv4_id_domain']
    self.udp = parameters['udp']
    self.tcp = parameters['tcp']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)