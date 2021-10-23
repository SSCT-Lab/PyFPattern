def reconnect_host_to_vcenter(self):
    reconnecthost_args = {
        
    }
    reconnecthost_args['reconnectSpec'] = vim.HostSystem.ReconnectSpec()
    reconnecthost_args['reconnectSpec'].syncState = True
    if ((self.esxi_username is not None) or (self.esxi_password is not None)):
        reconnecthost_args['cnxSpec'] = self.get_host_connect_spec()
        for count in range(0, 2):
            try:
                task = self.host.ReconnectHost_Task(**reconnecthost_args)
                (success, result) = wait_for_task(task)
                return (success, result)
            except TaskError as task_error_exception:
                task_error = task_error_exception.args[0]
                if ((self.esxi_ssl_thumbprint == '') and isinstance(task_error, vim.fault.SSLVerifyFault)):
                    reconnecthost_args['cnxSpec'].sslThumbprint = task_error.thumbprint
                else:
                    self.module.fail_json(msg=('Failed to reconnect host %s to vCenter: %s' % (self.esxi_hostname, to_native(task_error.msg))))
        self.module.fail_json(msg=('Failed to reconnect host %s to vCenter' % self.esxi_hostname))
    else:
        try:
            task = self.host.ReconnectHost_Task(**reconnecthost_args)
            (success, result) = wait_for_task(task)
            return (success, result)
        except TaskError as task_error_exception:
            task_error = task_error_exception.args[0]
            self.module.fail_json(msg=('Failed to reconnect host %s to vCenter due to %s' % (self.esxi_hostname, to_native(task_error.msg))))