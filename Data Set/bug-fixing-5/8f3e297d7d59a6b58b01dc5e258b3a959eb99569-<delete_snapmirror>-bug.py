def delete_snapmirror(self):
    '\n        Delete a SnapMirror relationship\n        #1. Quiesce the SnapMirror relationship at destination\n        #2. Break the SnapMirror relationship at the source\n        #3. Release the SnapMirror at destination\n        #4. Delete SnapMirror at destination\n        '
    if (not self.parameters.get('source_hostname')):
        self.module.fail_json(msg='Missing parameters for delete: Please specify the source cluster to release the SnapMirror relation')
    if self.parameters.get('source_username'):
        self.module.params['username'] = self.parameters['dest_username']
    if self.parameters.get('source_password'):
        self.module.params['password'] = self.parameters['dest_password']
    self.source_server = netapp_utils.setup_ontap_zapi(module=self.module)
    self.snapmirror_quiesce()
    self.snapmirror_break()
    if self.get_destination():
        self.snapmirror_release()
    self.snapmirror_delete()