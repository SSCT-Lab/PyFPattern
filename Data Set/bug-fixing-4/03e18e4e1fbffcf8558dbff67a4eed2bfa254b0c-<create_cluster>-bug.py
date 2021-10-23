def create_cluster(self):
    '\n        Create Cluster\n        '
    try:
        self.sfe.create_cluster(mvip=self.management_virtual_ip, svip=self.storage_virtual_ip, rep_count=self.replica_count, username=self.cluster_admin_username, password=self.cluster_admin_password, accept_eula=self.accept_eula, nodes=self.nodes, attributes=self.attributes)
    except Exception as exception_object:
        self.module.fail_json(msg=('Error create cluster %s' % to_native(exception_object)), exception=traceback.format_exc())