def reconnect_host_to_vcenter(self):
    reconnecthost_args = {
        
    }
    reconnecthost_args['reconnectSpec'] = vim.HostSystem.ReconnectSpec()
    reconnecthost_args['reconnectSpec'].syncState = True
    if ((self.esxi_username is not None) or (self.esxi_password is not None)):
        reconnecthost_args['cnxSpec'] = vim.host.ConnectSpec()
        reconnecthost_args['cnxSpec'].hostName = self.esxi_hostname
        reconnecthost_args['cnxSpec'].userName = self.esxi_username
        reconnecthost_args['cnxSpec'].password = self.esxi_password
        reconnecthost_args['cnxSpec'].force = True
        reconnecthost_args['cnxSpec'].sslThumbprint = ''
        try:
            task = self.host.ReconnectHost_Task(**reconnecthost_args)
            (success, result) = wait_for_task(task)
            return (success, result)
        except TaskError as add_task_error:
            ssl_verify_fault = add_task_error.args[0]
            reconnecthost_args['cnxSpec'].sslThumbprint = ssl_verify_fault.thumbprint
    task = self.host.ReconnectHost_Task(**reconnecthost_args)
    (success, result) = wait_for_task(task)
    return (success, result)