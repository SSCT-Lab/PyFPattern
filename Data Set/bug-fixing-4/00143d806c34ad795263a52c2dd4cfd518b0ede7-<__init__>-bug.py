def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), snapshot=dict(required=True, type='str'), volume=dict(required=True, type='str'), async_bool=dict(required=False, type='bool', default=False), comment=dict(required=False, type='str'), snapmirror_label=dict(required=False, type='str'), ignore_owners=dict(required=False, type='bool', default=False), snapshot_instance_uuid=dict(required=False, type='str'), vserver=dict(required=True, type='str'), new_comment=dict(required=False, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.snapshot = parameters['snapshot']
    self.vserver = parameters['vserver']
    self.volume = parameters['volume']
    self.async_bool = parameters['async_bool']
    self.comment = parameters['comment']
    self.snapmirror_label = parameters['snapmirror_label']
    self.ignore_owners = parameters['ignore_owners']
    self.snapshot_instance_uuid = parameters['snapshot_instance_uuid']
    self.new_comment = parameters['new_comment']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)
    return