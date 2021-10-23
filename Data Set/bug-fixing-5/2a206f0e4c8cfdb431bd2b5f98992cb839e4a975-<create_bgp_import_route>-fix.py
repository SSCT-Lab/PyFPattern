def create_bgp_import_route(self, **kwargs):
    ' create_bgp_import_route '
    module = kwargs['module']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    import_protocol = module.params['import_protocol']
    import_process_id = module.params['import_process_id']
    if ((import_protocol == 'direct') or (import_protocol == 'static')):
        import_process_id = '0'
    conf_str = (CE_CREATE_BGP_IMPORT_ROUTE % (vrf_name, af_type, import_protocol, import_process_id))
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Create bgp import route failed.')
    cmds = []
    cmd = ('import-route %s %s' % (import_protocol, import_process_id))
    if ((import_protocol == 'direct') or (import_protocol == 'static')):
        cmd = ('import-route %s' % import_protocol)
    cmds.append(cmd)
    return cmds