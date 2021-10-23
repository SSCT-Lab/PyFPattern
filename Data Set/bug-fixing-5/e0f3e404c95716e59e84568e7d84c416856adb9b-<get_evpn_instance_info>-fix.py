def get_evpn_instance_info(self):
    'Get current EVPN instance information'
    if (not self.bridge_domain_id):
        self.module.fail_json(msg='Error: The value of bridge_domain_id cannot be empty.')
    self.evpn_info['route_distinguisher'] = None
    self.evpn_info['vpn_target_import'] = list()
    self.evpn_info['vpn_target_export'] = list()
    self.evpn_info['vpn_target_both'] = list()
    self.evpn_info['evpn_inst'] = 'enable'
    xml_str = (CE_NC_GET_EVPN_CONFIG % (self.bridge_domain_id, self.bridge_domain_id))
    xml_str = get_nc_config(self.module, xml_str)
    if ('<data/>' in xml_str):
        self.evpn_info['evpn_inst'] = 'disable'
        return
    xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    evpn_inst = root.find('evpn/evpnInstances/evpnInstance')
    if evpn_inst:
        for eles in evpn_inst:
            if (eles.tag in ['evpnAutoRD', 'evpnRD', 'evpnRTs', 'evpnAutoRTs']):
                if ((eles.tag == 'evpnAutoRD') and (eles.text == 'true')):
                    self.evpn_info['route_distinguisher'] = 'auto'
                elif ((eles.tag == 'evpnRD') and (self.evpn_info['route_distinguisher'] != 'auto')):
                    self.evpn_info['route_distinguisher'] = eles.text
                elif (eles.tag == 'evpnRTs'):
                    self.get_all_evpn_rts(eles)
                elif (eles.tag == 'evpnAutoRTs'):
                    self.get_all_evpn_autorts(eles)
        self.process_rts_info()