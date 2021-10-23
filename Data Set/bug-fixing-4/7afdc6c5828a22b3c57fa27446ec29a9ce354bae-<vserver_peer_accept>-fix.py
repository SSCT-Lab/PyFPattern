def vserver_peer_accept(self):
    '\n        Accept a vserver peer at destination\n        '
    vserver_peer_accept = netapp_utils.zapi.NaElement.create_node_with_children('vserver-peer-accept', **{
        'peer-vserver': self.parameters['vserver'],
        'vserver': self.parameters['peer_vserver'],
    })
    try:
        if (self.parameters.get('dest_hostname') is not None):
            self.dest_server.invoke_successfully(vserver_peer_accept, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error accepting vserver peer %s: %s' % (self.parameters['peer_vserver'], to_native(error))), exception=traceback.format_exc())