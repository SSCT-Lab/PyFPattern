def create_volume(self):
    'Create ONTAP volume'
    if (self.aggregate_name is None):
        self.module.fail_json(msg=('Error provisioning volume %s:                                   aggregate_name is required' % self.name))
    options = {
        'volume': self.name,
        'containing-aggr-name': self.aggregate_name,
        'size': str(self.size),
    }
    if (self.percent_snapshot_space is not None):
        options['percentage-snapshot-reserve'] = self.percent_snapshot_space
    if (self.type is not None):
        options['volume-type'] = self.type
    if (self.policy is not None):
        options['export-policy'] = self.policy
    if (self.junction_path is not None):
        options['junction-path'] = self.junction_path
    if (self.space_guarantee is not None):
        options['space-reserve'] = self.space_guarantee
    if (self.volume_security_style is not None):
        options['volume-security-style'] = self.volume_security_style
    volume_create = netapp_utils.zapi.NaElement.create_node_with_children('volume-create', **options)
    try:
        self.server.invoke_successfully(volume_create, enable_tunneling=True)
        self.ems_log_event('create')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error provisioning volume %s                                   of size %s: %s' % (self.name, self.size, to_native(error))), exception=traceback.format_exc())