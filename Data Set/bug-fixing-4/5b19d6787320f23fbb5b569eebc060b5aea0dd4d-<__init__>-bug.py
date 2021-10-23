def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, type='str', choices=['present', 'absent'], default='present'), policy_name=dict(required=True, type='str'), protocol=dict(required=False, type='str', default='any', choices=['any', 'nfs', 'nfs3', 'nfs4', 'cifs', 'flexcache']), client_match=dict(required=False, type='str'), ro_rule=dict(required=False, type='str', default=None, choices=['any', 'none', 'never', 'krb5', 'krb5i', 'krb5p', 'ntlm', 'sys']), rw_rule=dict(required=False, type='str', default=None, choices=['any', 'none', 'never', 'krb5', 'krb5i', 'krb5p', 'ntlm', 'sys']), super_user_security=dict(required=False, type='str', default=None, choices=['any', 'none', 'never', 'krb5', 'krb5i', 'krb5p', 'ntlm', 'sys']), allow_suid=dict(required=False, choices=['True', 'False']), rule_index=dict(required=False, type='int', default=None), vserver=dict(required=True, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['client_match', 'ro_rule', 'rw_rule']), ('state', 'absent', ['client_match'])], supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.policy_name = parameters['policy_name']
    self.protocol = parameters['protocol']
    self.client_match = parameters['client_match']
    self.ro_rule = parameters['ro_rule']
    self.rw_rule = parameters['rw_rule']
    self.allow_suid = parameters['allow_suid']
    self.vserver = parameters['vserver']
    self.super_user_security = parameters['super_user_security']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)