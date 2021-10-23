def modify_cluster_ha(self, configure):
    '\n        Enable or disable HA on cluster\n        '
    cluster_ha_modify = netapp_utils.zapi.NaElement.create_node_with_children('cluster-ha-modify', **{
        'ha-configured': configure,
    })
    try:
        self.server.invoke_successfully(cluster_ha_modify, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error modifying cluster HA to %s: %s' % (configure, to_native(error))), exception=traceback.format_exc())