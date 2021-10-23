def create_vserver(self):
    options = {
        'vserver-name': self.name,
        'root-volume': self.root_volume,
    }
    if (self.root_volume_aggregate is not None):
        options['root-volume-aggregate'] = self.root_volume_aggregate
    if (self.root_volume_security_style is not None):
        options['root-volume-security-style'] = self.root_volume_security_style
    if (self.language is not None):
        options['language'] = self.language
    if (self.ipspace is not None):
        options['ipspace'] = self.ipspace
    if (self.snapshot_policy is not None):
        options['snapshot-policy'] = self.snapshot_policy
    if (self.subtype is not None):
        options['vserver-subtype'] = self.subtype
    vserver_create = netapp_utils.zapi.NaElement.create_node_with_children('vserver-create', **options)
    try:
        self.server.invoke_successfully(vserver_create, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error provisioning SVM %s                                   with root volume %s on aggregate %s: %s' % (self.name, self.root_volume, self.root_volume_aggregate, to_native(e))), exception=traceback.format_exc())