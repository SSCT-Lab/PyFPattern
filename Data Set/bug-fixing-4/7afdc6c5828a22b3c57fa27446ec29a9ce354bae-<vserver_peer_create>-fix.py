def vserver_peer_create(self):
    '\n        Create a vserver peer\n        '
    if (self.parameters.get('applications') is None):
        self.module.fail_json(msg='applications parameter is missing')
    if ((self.parameters.get('peer_cluster') is not None) and (self.parameters.get('dest_hostname') is None)):
        self.module.fail_json(msg='dest_hostname is required for peering a vserver in remote cluster')
    if (self.parameters.get('peer_cluster') is None):
        self.parameters['peer_cluster'] = self.get_peer_cluster_name()
    vserver_peer_create = netapp_utils.zapi.NaElement.create_node_with_children('vserver-peer-create', **{
        'peer-vserver': self.parameters['peer_vserver'],
        'vserver': self.parameters['vserver'],
        'peer-cluster': self.parameters['peer_cluster'],
    })
    applications = netapp_utils.zapi.NaElement('applications')
    for application in self.parameters['applications']:
        applications.add_new_child('vserver-peer-application', application)
    vserver_peer_create.add_child_elem(applications)
    try:
        self.server.invoke_successfully(vserver_peer_create, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error creating vserver peer %s: %s' % (self.parameters['vserver'], to_native(error))), exception=traceback.format_exc())