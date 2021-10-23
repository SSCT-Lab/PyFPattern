

def add_host_to_vcenter(self):
    host_connect_spec = self.get_host_connect_spec()
    as_connected = self.params.get('add_connected')
    esxi_license = None
    resource_pool = None
    for count in range(0, 2):
        try:
            task = None
            if self.folder:
                task = self.folder.AddStandaloneHost(spec=host_connect_spec, addConnected=as_connected)
            elif self.cluster:
                task = self.cluster.AddHost_Task(host_connect_spec, as_connected, resource_pool, esxi_license)
            (success, result) = wait_for_task(task)
            return (success, result)
        except TaskError as task_error_exception:
            task_error = task_error_exception.args[0]
            if ((self.esxi_ssl_thumbprint == '') and isinstance(task_error, vim.fault.SSLVerifyFault)):
                host_connect_spec.sslThumbprint = task_error.thumbprint
            else:
                self.module.fail_json(msg=('Failed to add host %s to vCenter: %s' % (self.esxi_hostname, to_native(task_error))))
        except vmodl.fault.NotSupported:
            self.module.fail_json(msg=('Failed to add host %s to vCenter as host is being added to a folder %s whose childType property does not contain "ComputeResource".' % (self.esxi_hostname, self.folder_name)))
        except Exception as generic_exc:
            self.module.fail_json(msg=('Failed to add host %s to vCenter: %s' % (self.esxi_hostname, to_native(generic_exc))))
    self.module.fail_json(msg=('Failed to add host %s to vCenter' % self.esxi_hostname))
