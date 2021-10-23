def __init__(self, module):
    super(VMwareHost, self).__init__(module)
    self.datacenter_name = module.params['datacenter_name']
    self.cluster_name = module.params['cluster_name']
    self.esxi_hostname = module.params['esxi_hostname']
    self.esxi_username = module.params['esxi_username']
    self.esxi_password = module.params['esxi_password']
    self.state = module.params['state']
    self.esxi_ssl_thumbprint = module.params.get('esxi_ssl_thumbprint', '')
    self.cluster = None
    self.host = None