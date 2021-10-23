def snapmirror_initialize(self):
    '\n        Initialize SnapMirror based on relationship type\n        '
    current = self.snapmirror_get()
    if (current['mirror_state'] != 'snapmirrored'):
        initialize_zapi = 'snapmirror-initialize'
        if (self.parameters.get('relationship_type') and (self.parameters['relationship_type'] == 'load_sharing')):
            initialize_zapi = 'snapmirror-initialize-ls-set'
            options = {
                'source-location': self.parameters['source_path'],
            }
        else:
            options = {
                'destination-location': self.parameters['destination_path'],
            }
        snapmirror_init = netapp_utils.zapi.NaElement.create_node_with_children(initialize_zapi, **options)
        try:
            self.server.invoke_successfully(snapmirror_init, enable_tunneling=True)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg=('Error initializing SnapMirror : %s' % to_native(error)), exception=traceback.format_exc())