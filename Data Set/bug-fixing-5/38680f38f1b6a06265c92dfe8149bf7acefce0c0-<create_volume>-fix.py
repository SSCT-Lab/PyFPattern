def create_volume(self):
    'Create ONTAP volume'
    if (self.parameters.get('aggregate_name') is None):
        self.module.fail_json(msg=('Error provisioning volume %s:                                   aggregate_name is required' % self.parameters['name']))
    options = {
        'volume': self.parameters['name'],
        'containing-aggr-name': self.parameters['aggregate_name'],
        'size': str(self.parameters['size']),
    }
    if self.parameters.get('percent_snapshot_space'):
        options['percentage-snapshot-reserve'] = self.parameters['percent_snapshot_space']
    if self.parameters.get('type'):
        options['volume-type'] = self.parameters['type']
    if self.parameters.get('policy'):
        options['export-policy'] = self.parameters['policy']
    if self.parameters.get('junction_path'):
        options['junction-path'] = self.parameters['junction_path']
    if self.parameters.get('space_guarantee'):
        options['space-reserve'] = self.parameters['space_guarantee']
    if self.parameters.get('volume_security_style'):
        options['volume-security-style'] = self.parameters['volume_security_style']
    volume_create = netapp_utils.zapi.NaElement.create_node_with_children('volume-create', **options)
    try:
        self.server.invoke_successfully(volume_create, enable_tunneling=True)
        self.ems_log_event('volume-create')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error provisioning volume %s                                   of size %s: %s' % (self.parameters['name'], self.parameters['size'], to_native(error))), exception=traceback.format_exc())