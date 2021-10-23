def set_protocol_option(self, required_keys):
    ' set protocols for create '
    if (self.parameters.get('protocols') is not None):
        data_protocols_obj = netapp_utils.zapi.NaElement('data-protocols')
        for protocol in self.parameters.get('protocols'):
            if (protocol.lower() == 'fc-nvme'):
                required_keys.remove('address')
                required_keys.remove('home_port')
                required_keys.remove('netmask')
                not_required_params = set(['address', 'netmask', 'firewall_policy'])
                if (not not_required_params.isdisjoint(set(self.parameters.keys()))):
                    self.module.fail_json(msg=('Error: Following parameters for creating interface are not supported for data-protocol fc-nvme: %s' % ', '.join(not_required_params)))
            data_protocols_obj.add_new_child('data-protocol', protocol)
        return data_protocols_obj
    return None