

def set_ospf_interface(self):
    'set interface ospf enable, and set its ospf attributes'
    xml_intf = (CE_NC_XML_SET_IF_NAME % self.interface)
    self.updates_cmd.append(('ospf %s' % self.process_id))
    self.updates_cmd.append(('area %s' % self.get_area_ip()))
    if self.silent_interface:
        xml_intf += (CE_NC_XML_SET_SILENT % str(self.silent_interface).lower())
        if self.silent_interface:
            self.updates_cmd.append(('silent-interface %s' % self.interface))
        else:
            self.updates_cmd.append(('undo silent-interface %s' % self.interface))
    self.updates_cmd.append(('interface %s' % self.interface))
    self.updates_cmd.append(('ospf enable process %s area %s' % (self.process_id, self.get_area_ip())))
    if self.cost:
        xml_intf += (CE_NC_XML_SET_COST % self.cost)
        self.updates_cmd.append(('ospf cost %s' % self.cost))
    if self.hello_interval:
        xml_intf += (CE_NC_XML_SET_HELLO % self.hello_interval)
        self.updates_cmd.append(('ospf timer hello %s' % self.hello_interval))
    if self.dead_interval:
        xml_intf += (CE_NC_XML_SET_DEAD % self.dead_interval)
        self.updates_cmd.append(('ospf timer dead %s' % self.dead_interval))
    if self.auth_mode:
        xml_intf += (CE_NC_XML_SET_AUTH_MODE % self.auth_mode)
        if (self.auth_mode == 'none'):
            self.updates_cmd.append('undo ospf authentication-mode')
        else:
            self.updates_cmd.append(('ospf authentication-mode %s' % self.auth_mode))
        if ((self.auth_mode == 'simple') and self.auth_text_simple):
            xml_intf += (CE_NC_XML_SET_AUTH_TEXT_SIMPLE % self.auth_text_simple)
            self.updates_cmd.pop()
            self.updates_cmd.append(('ospf authentication-mode %s %s' % (self.auth_mode, self.auth_text_simple)))
        elif ((self.auth_mode in ['hmac-sha256', 'md5', 'hmac-md5']) and self.auth_key_id):
            xml_intf += (CE_NC_XML_SET_AUTH_MD5 % (self.auth_key_id, self.auth_text_md5))
            self.updates_cmd.pop()
            self.updates_cmd.append(('ospf authentication-mode %s %s %s' % (self.auth_mode, self.auth_key_id, self.auth_text_md5)))
        else:
            pass
    xml_str = (CE_NC_XML_BUILD_PROCESS % (self.process_id, self.get_area_ip(), (CE_NC_XML_BUILD_MERGE_INTF % xml_intf)))
    self.netconf_set_config(xml_str, 'SET_INTERFACE_OSPF')
    self.changed = True
