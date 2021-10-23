def modify_service_processor_network(self):
    '\n        Modify a service processor network\n        '
    service_obj = netapp_utils.zapi.NaElement('service-processor-network-modify')
    service_obj.add_new_child('node', self.node)
    service_obj.add_new_child('address-type', self.address_type)
    service_obj.add_new_child('is-enabled', self.is_enabled)
    if self.dhcp:
        service_obj.add_new_child('dhcp', self.dhcp)
    if self.gateway_ip_address:
        service_obj.add_new_child('gateway-ip-address', self.gateway_ip_address)
    if self.ip_address:
        service_obj.add_new_child('ip-address', self.ip_address)
    if self.netmask:
        service_obj.add_new_child('netmask', self.netmask)
    if (self.prefix_length is not None):
        service_obj.add_new_child('prefix-length', str(self.prefix_length))
    try:
        result = self.server.invoke_successfully(service_obj, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error modifying                                   service processor network: %s' % to_native(error)), exception=traceback.format_exc())