def add_host_to_vcenter(self):
    host_connect_spec = vim.host.ConnectSpec()
    host_connect_spec.hostName = self.esxi_hostname
    host_connect_spec.userName = self.esxi_username
    host_connect_spec.password = self.esxi_password
    host_connect_spec.force = True
    host_connect_spec.sslThumbprint = self.esxi_ssl_thumbprint
    as_connected = True
    esxi_license = None
    resource_pool = None
    for count in range(0, 2):
        try:
            task = self.cluster.AddHost_Task(host_connect_spec, as_connected, resource_pool, esxi_license)
            (success, result) = wait_for_task(task)
            return (success, result)
        except TaskError as task_error_exception:
            task_error = task_error_exception.args[0]
            if ((self.esxi_ssl_thumbprint == '') and isinstance(task_error, vim.fault.SSLVerifyFault)):
                host_connect_spec.sslThumbprint = task_error.thumbprint
            else:
                self.module.fail_json(msg=('Failed to add host %s to vCenter: %s' % (self.esxi_hostname, to_native(task_error.msg))))
    self.module.fail_json(msg=('Failed to add host %s to vCenter' % self.esxi_hostname))