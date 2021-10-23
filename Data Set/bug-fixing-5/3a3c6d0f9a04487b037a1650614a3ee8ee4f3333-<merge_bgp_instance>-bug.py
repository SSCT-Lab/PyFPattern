def merge_bgp_instance(self, **kwargs):
    ' merge_bgp_instance '
    module = kwargs['module']
    conf_str = CE_MERGE_BGP_INSTANCE_HEADER
    vrf_name = module.params['vrf_name']
    conf_str += ('<vrfName>%s</vrfName>' % vrf_name)
    conf_str += CE_MERGE_BGP_INSTANCE_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Merge bgp instance failed.')