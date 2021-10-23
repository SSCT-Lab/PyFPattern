def modify_interface(self, modify):
    '\n        Modify the interface.\n        '
    options = {
        'interface-name': self.parameters['interface_name'],
        'vserver': self.parameters['vserver'],
    }
    self.set_options(options, modify)
    interface_modify = netapp_utils.zapi.NaElement.create_node_with_children('net-interface-modify', **options)
    try:
        self.server.invoke_successfully(interface_modify, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as err:
        self.module.fail_json(msg=('Error modifying interface %s: %s' % (self.parameters['interface_name'], to_native(err))), exception=traceback.format_exc())