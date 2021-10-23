def add_host_to_vcenter(self):
    if ((self.esxi_username is None) or (self.esxi_password is None)):
        self.module.fail_json(msg='esxi_username and esxi_password are required to add a host')
    host_connect_spec = vim.host.ConnectSpec()
    host_connect_spec.hostName = self.esxi_hostname
    host_connect_spec.userName = self.esxi_username
    host_connect_spec.password = self.esxi_password
    host_connect_spec.force = True
    host_connect_spec.sslThumbprint = ''
    as_connected = True
    esxi_license = None
    resource_pool = None
    try:
        task = self.cluster.AddHost_Task(host_connect_spec, as_connected, resource_pool, esxi_license)
        (success, result) = wait_for_task(task)
        return (success, result)
    except TaskError as add_task_error:
        ssl_verify_fault = add_task_error.args[0]
        host_connect_spec.sslThumbprint = ssl_verify_fault.thumbprint
    task = self.cluster.AddHost_Task(host_connect_spec, as_connected, resource_pool, esxi_license)
    (success, result) = wait_for_task(task)
    return (success, result)