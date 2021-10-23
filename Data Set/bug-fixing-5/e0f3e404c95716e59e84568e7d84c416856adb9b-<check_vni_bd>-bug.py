def check_vni_bd(self):
    'Check whether vxlan vni is configured in BD view'
    xml_str = (CE_NC_GET_VNI_BD % self.bridge_domain_id)
    xml_str = get_nc_config(self.module, xml_str)
    if ('<data/>' in xml_str):
        self.module.fail_json(msg='Error: The vxlan vni is not configured or the bridge domain id is invalid.')