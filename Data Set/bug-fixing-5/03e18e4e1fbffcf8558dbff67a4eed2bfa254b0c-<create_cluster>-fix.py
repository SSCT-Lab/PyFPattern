def create_cluster(self):
    '\n        Create Cluster\n        '
    options = {
        'mvip': self.management_virtual_ip,
        'svip': self.storage_virtual_ip,
        'rep_count': self.replica_count,
        'accept_eula': self.accept_eula,
        'nodes': self.nodes,
        'attributes': self.attributes,
    }
    if (self.cluster_admin_username is not None):
        options['username'] = self.cluster_admin_username
    if (self.cluster_admin_password is not None):
        options['password'] = self.cluster_admin_password
    try:
        self.sfe.create_cluster(**options)
    except Exception as exception_object:
        self.module.fail_json(msg=('Error create cluster %s' % to_native(exception_object)), exception=traceback.format_exc())