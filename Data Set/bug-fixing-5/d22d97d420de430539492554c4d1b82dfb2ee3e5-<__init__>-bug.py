def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), service_state=dict(required=False, choices=['stopped', 'started']), cifs_server_name=dict(required=False, type='str'), workgroup=dict(required=False, type='str', default=None), domain=dict(required=False, type='str'), admin_user_name=dict(required=False, type='str'), admin_password=dict(required=False, type='str'), vserver=dict(required=True, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    params = self.module.params
    self.state = params['state']
    self.cifs_server_name = params['cifs_server_name']
    self.workgroup = params['workgroup']
    self.domain = params['domain']
    self.vserver = params['vserver']
    self.service_state = params['service_state']
    self.admin_user_name = params['admin_user_name']
    self.admin_password = params['admin_password']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)