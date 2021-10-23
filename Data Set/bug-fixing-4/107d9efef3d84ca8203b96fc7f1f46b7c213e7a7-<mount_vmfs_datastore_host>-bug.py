def mount_vmfs_datastore_host(self):
    if (self.module.check_mode is False):
        ds_path = ('/vmfs/devices/disks/' + str(self.vmfs_device_name))
        host_ds_system = self.esxi.configManager.datastoreSystem
        ds_system = vim.host.DatastoreSystem
        error_message_mount = ('Cannot mount datastore %s on host %s' % (self.datastore_name, self.esxi_hostname))
        try:
            vmfs_ds_options = ds_system.QueryVmfsDatastoreCreateOptions(host_ds_system, ds_path, self.vmfs_version)
            vmfs_ds_options[0].spec.vmfs.volumeName = self.datastore_name
            ds = ds_system.CreateVmfsDatastore(host_ds_system, vmfs_ds_options[0].spec)
        except (vim.fault.NotFound, vim.fault.DuplicateName, vim.fault.HostConfigFault, vmodl.fault.InvalidArgument) as fault:
            self.module.fail_json(msg=('%s : %s' % (error_message_mount, to_native(fault.msg))))
        except Exception as e:
            self.module.fail_json(msg=('%s : %s' % (error_message_mount, to_native(e))))
    self.module.exit_json(changed=True, result=('Datastore %s on host %s' % (self.datastore_name, self.esxi_hostname)))